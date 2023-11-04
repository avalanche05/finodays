from typing import List

from app import models, schemas
from .user import get_public_user
from .cfa_image import get_cfa_image


def get_cfa(db_cfa: models.Cfa) -> schemas.Cfa:
    cfa = schemas.Cfa(
        token=db_cfa.token,
        cfa_image=get_cfa_image(db_cfa.cfa_image),
        user=get_public_user(db_cfa.user),
    )

    return cfa


def get_cfas(db_cfas: List[models.Cfa]) -> List[schemas.Cfa]:
    return [get_cfa(db_cfa) for db_cfa in db_cfas]
