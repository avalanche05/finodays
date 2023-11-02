from typing import Type, List

from app.models import cfa_image as db_model_cfa_image
from app.schemas import CfaImage
from .user import get_public_user


def get_cfa_image(db_cfa_image: db_model_cfa_image.CfaImage) -> CfaImage:
    cfa_image = CfaImage(
        id=db_cfa_image.id,
        title=db_cfa_image.title,
        count=db_cfa_image.count,
        description=db_cfa_image.description,
        user=get_public_user(db_cfa_image.user),
    )

    return cfa_image


def get_cfa_images(db_cfa_images: List[db_model_cfa_image.CfaImage]):
    return [get_cfa_image(db_cfa_image) for db_cfa_image in db_cfa_images]
