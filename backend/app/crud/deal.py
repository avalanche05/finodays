from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas, errors


def create_deal(db: Session, payload: schemas.DealCreateRequest, initiator_id: int):
    """Создание Deal"""

    db_deal = models.Deal(
        initiator_id=initiator_id,
        host_id=payload.host_id,
        initiator_items=payload.initiator_items,
        host_items=payload.host_items,
        is_active=True,
        is_accepted=False
    )

    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)

    return db_deal


def unable_deal(db: Session, user_id: int, deal_id: int):
    """Закрытие предложения"""
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()

    if deal is None:
        raise errors.DealNotFoundError()

    if deal.initiator_id != user_id and deal.host_id != user_id:
        raise errors.DealNotFoundError()

    deal.is_active = False

    db.commit()


def accept_deal(db: Session, user_id: int, deal_id: int):
    """Принятие предложения"""
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()

    if deal is None:
        raise errors.DealNotFoundError()

    if deal.host_id != user_id:
        raise errors.DealNotFoundError()

    deal.is_active = False
    deal.is_accepted = True

    db.commit()


def get_deal(db: Session, deal_id: int):
    """Получение сделки"""
    db_deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()

    if db_deal is None:
        raise errors.DealNotFoundError()

    return db_deal


def get_in_deals(db: Session, user_id: int):
    """Получение входящих сделок"""

    deals = db.query(models.Deal).filter(and_(
        models.Deal.host_id == user_id,
        models.Deal.is_active == True)).all()

    return deals


def get_out_deals(db: Session, user_id: int):
    """Получение исходящих сделок"""

    deals = db.query(models.Deal).filter(
        models.Deal.initiator_id == user_id,
        models.Deal.is_active is True).all()

    return deals
