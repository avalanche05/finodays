from typing import List

from sqlalchemy.orm import Session

from app import schemas, models


def get_all_cfa_by_cfa_image(db: Session, cfa_image_id: int) -> List[models.Cfa]:
    """Список всех Cfa конкретного CfaImage"""

    cfas = db.query(models.Cfa).filter(models.Cfa.cfa_image_id == cfa_image_id).all()

    return cfas


def get_all_cfa_by_user_id(db: Session, user_id: int) -> List[models.Cfa]:
    """Список всех Cfa конкретного пользователя"""

    cfas = db.query(models.Cfa).filter(models.Cfa.user_id == user_id, models.Cfa.offer_id.is_(None)).all()

    return cfas


def get_user_cfa_by_cfa_image(db: Session, user_id: int, cfa_image_id: int, count: int) -> List[models.Cfa]:
    cfas = db.query(models.Cfa).filter(
        models.Cfa.user_id == user_id,
        models.Cfa.cfa_image_id == cfa_image_id,
        models.Cfa.offer_id.is_(None)).limit(count).all()

    return cfas


def get_cfa_by_token(db: Session, token: str) -> models.Cfa:
    cfa = db.get(models.Cfa, token)

    return cfa


def get_cfa_history(db: Session, token: str) -> List[models.Trade]:
    db_deals = db.query(models.Trade).filter(models.Trade.cfa_token == token).all()
    return db_deals
