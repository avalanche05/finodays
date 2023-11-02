from datetime import datetime
from typing import List

from sqlalchemy.orm import Session, Mapper
from sqlalchemy import update, and_
from app import models, schemas, errors


def create_offer(db: Session, offer_create: schemas.OfferCreateRequest, user_id: int):
    cfas = db.query(models.Cfa) \
        .filter(models.Cfa.offer_id.is_(None),
                models.Cfa.cfa_image_id == offer_create.cfa_image_id,
                models.Cfa.user_id == user_id) \
        .limit(offer_create.count) \
        .all()

    if len(cfas) < offer_create.count:
        raise errors.NotEnoughCfa()

    db_offer = models.Offer(
        cfa_image_id=offer_create.cfa_image_id,
        count=offer_create.count,
        price=offer_create.price,
        seller_id=user_id,
    )

    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)

    for cfa in cfas:
        cfa.offer_id = db_offer.id

    db.add_all(cfas)

    db.commit()

    return db_offer


def buy_offer(db: Session, offer_buy: schemas.OfferBuyRequest, offer_id: int, db_user: models.User):
    db_user = db.get(models.User, db_user.id)
    try:
        db_offer = db.get(models.Offer, offer_id)
    except Exception as e:
        raise errors.OfferNotFoundError(e)

    if db_user.balance < db_offer.price * offer_buy.count:
        raise errors.BuyOfferError("Not enough money")

    if db_offer.count < offer_buy.count:
        raise errors.OfferCountNotEnough()

    current_time = datetime.now()

    trades = []
    cfas = db.query(models.Cfa) \
        .filter(models.Cfa.offer_id == db_offer.id) \
        .limit(offer_buy.count) \
        .all()
    for cfa in cfas:
        cfa.offer_id = None
        cfa.user_id = db_user.id
        trades.append(models.Trade(
            cfa_token=cfa.token,
            price=db_offer.price,
            buyer_id=db_user.id,
            seller_id=db_offer.seller_id,
            created_at=current_time
        ))

    db_offer.count -= offer_buy.count
    db_user.balance -= db_offer.price * offer_buy.count
    db.add(db_offer)
    db.add(db_user)

    db.commit()
    db.add_all(trades)
    db.add_all(cfas)
    db.commit()


def get_active_offer_list(db: Session, cfa_image_id: int) -> List[models.Offer]:
    offers = db.query(models.Offer).filter(and_(models.Offer.cfa_image_id == cfa_image_id,
                                                models.Offer.count > 0)).all()

    return offers


def get_offer_list(db: Session, cfa_image_id: int) -> List[models.Offer]:
    offers = db.query(models.Offer).filter(models.Offer.cfa_image_id == cfa_image_id).all()

    return offers


def get_user_offers(db: Session, user_id: int) -> List[models.Offer]:
    offers = db.query(models.Offer).filter(models.Offer.seller_id == user_id, models.Offer.count > 0).all()

    return offers


def cancel_offer(db: Session, offer_id: int, db_user: models.User):
    try:
        db_offer: models.Offer = db.get(models.Offer, offer_id)
    except Exception as e:
        raise errors.OfferNotFoundError(e)

    if db_offer.seller_id != db_user.id:
        raise errors.CancelOfferError(f"User with id {db_user.id} is not owner of offer with id {offer_id}")

    db_offer.count = 0
    db.commit()

    stmt = update(models.Cfa).where(models.Cfa.offer_id == offer_id).values(offer_id=None)
    db.execute(stmt)
    db.commit()
