from typing import List

from app import models, schemas
from .cfa_image import get_cfa_image
from .user import get_public_user


def get_offer(db_offer: models.Offer) -> schemas.Offer:
    offer = schemas.Offer(
        id=db_offer.id,
        cfa_image=get_cfa_image(db_offer.cfa_image),
        count=db_offer.count,
        price=db_offer.price,
        seller=get_public_user(db_offer.seller)
    )

    return offer


def get_offers(db_offers: List[models.Offer]) -> List[schemas.Offer]:
    return [get_offer(db_offer) for db_offer in db_offers]
