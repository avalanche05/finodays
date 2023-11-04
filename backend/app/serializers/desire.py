from typing import List

from app import models, schemas
from .cfa_image import get_cfa_image
from .user import get_public_user


def get_desire(db_desire: models.Desire):
    desire = schemas.Desire(
        id=db_desire.id,
        cfa_image=get_cfa_image(db_desire.cfa_image),
        count=db_desire.count,
        price=db_desire.price,
        buyer=get_public_user(db_desire.buyer),
    )

    return desire


def get_desires(db_desires: List[models.Desire]):
    desires = [get_desire(db_desire) for db_desire in db_desires]

    return desires
