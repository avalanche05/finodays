from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from requests import Session

from app import schemas, crud, serializers, models, errors
from app.dependencies import get_db, current_user

desire_router = APIRouter(
    prefix="/desire",
    tags=["Desire"],
)


@desire_router.get(path='/list/{cfa_image_id}')
def desire_list(cfa_image_id: int,
                db: Session = Depends(get_db),
                ) -> List[schemas.Desire]:
    db_desire = crud.desire_list(db, cfa_image_id)

    return serializers.get_desires(db_desire)


@desire_router.post(path='/create')
def create_desire(create_desire: schemas.DesireCreateRequest,
                  db: Session = Depends(get_db),
                  user: models.User = Depends(current_user)
                  ) -> schemas.Desire:
    db_desire = crud.create_desire(db, create_desire, user.id)

    return serializers.get_desire(db_desire)


@desire_router.post(path='/cancel/{desire_id}')
def cancel_desire(desire_id: int,
                  db: Session = Depends(get_db),
                  user: models.User = Depends(current_user)
                  ):
    try:
        crud.cancel_desire(db, desire_id, user)
    except errors.CancelDesireError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)


@desire_router.post(path='/sell/{desire_id}')
def sell_desire(desire_id: int,
                desire_sell: schemas.DesireSellRequest,
                db: Session = Depends(get_db),
                user: models.User = Depends(current_user)):
    crud.sell_desire(db, desire_sell, desire_id, user)
