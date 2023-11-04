from typing import List, Type

from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app import models, schemas, utils, errors


def create_cfa_image(db: Session, payload: schemas.CfaImageCreateRequest, db_user: models.User) -> models.CfaImage:
    """Создание Cfa-образа"""

    db_cfa_image = models.CfaImage(
        user_id=db_user.id,
        count=payload.count,
        title=payload.title,
        description=payload.description,
        cfas=[models.Cfa(token=utils.generate_bearer_token(64), user_id=db_user.id) for _ in range(payload.count)]
    )

    db.add(db_cfa_image)
    db.commit()
    db.refresh(db_cfa_image)

    return db_cfa_image


def get_all_cfa_images(db: Session) -> List[models.CfaImage]:
    """Список всех Cfa-образов"""

    db_cfa_images = db.query(models.CfaImage).all()

    return db_cfa_images


def get_cfa_image_price(db: Session, cfa_image_id: int):
    price = db.query(func.min(models.Offer.price)).filter(and_(
        models.Offer.count > 0, models.Offer.cfa_image_id == cfa_image_id)).scalar()

    return price


def get_cfa_image(db: Session, cfa_image_id) -> models.CfaImage:
    cfa_image = db.query(models.CfaImage).filter(models.CfaImage.id == cfa_image_id).first()

    if cfa_image is None:
        raise errors.CfaImageNotFoundError()

    return cfa_image
