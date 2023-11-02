from typing import Annotated, List, Tuple

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from requests import Session

from app import schemas, crud, serializers, errors, models, utils
from app.dependencies import get_db, current_user

cfa_image_router = APIRouter(
    prefix="/cfa-image",
    tags=['CfaImage']
)


@cfa_image_router.post(path="/create")
def create_cfa_image(cfa_image_create: schemas.CfaImageCreateRequest = Body(...),
                     user: models.User = Depends(current_user),
                     db: Session = Depends(get_db)
                     ) -> schemas.CfaImage:
    db_cfa_image = crud.create_cfa_image(db, cfa_image_create, user)

    return serializers.get_cfa_image(db_cfa_image)


@cfa_image_router.get(path="/list")
def list_cfa_images(db: Session = Depends(get_db)) -> List[schemas.CfaImage]:
    db_cfa_images = crud.get_all_cfa_images(db)

    return serializers.get_cfa_images(db_cfa_images)


@cfa_image_router.get("/price/{cfa_image_id}")
def cfa_image_price(cfa_image_id: int, db: Session = Depends(get_db)) -> schemas.CfaImagePrice:
    return schemas.CfaImagePrice(price=crud.get_cfa_image_price(db, cfa_image_id))


@cfa_image_router.get("/price-history/{cfa_image_id}")
def cfa_image_price_history(cfa_image_id: int, db: Session = Depends(get_db)) -> List[schemas.CfaImagePrice]:
    return utils.get_cfa_image_price_history(db, cfa_image_id, 96)[0]


@cfa_image_router.get("/buy-advice/{cfa_image_id}")
def cfa_image_buy_advice(cfa_image_id: int, db: Session = Depends(get_db)) -> schemas.CfaImageBuyAdvice:
    mins, maxs, latests = utils.get_cfa_image_price_history(db, cfa_image_id, 96)
    mins = [t.price for t in mins]
    maxs = [t.price for t in maxs]
    latests = [t.price for t in latests]

    result = utils.get_ishimoku_info(mins, maxs, latests)

    if result is None:
        return schemas.CfaImageBuyAdvice(is_buy=False, why={'en': 'Insufficient information', 'ru': "Недостаточно информации"})

    return schemas.CfaImageBuyAdvice(is_buy=result["is_buy"], why=result["why"])
