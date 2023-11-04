from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from requests import Session

from app import schemas, crud, serializers
from app.dependencies import get_db

cfa_router = APIRouter(
    prefix="/cfa",
    tags=['Cfa']
)


@cfa_router.get(path="/list/{cfa_image_id}")
def create_cfa_image(cfa_image_id: int,
                     db: Session = Depends(get_db)
                     ) -> List[schemas.Cfa]:
    db_cfas = crud.get_all_cfa_by_cfa_image(db, cfa_image_id)

    return serializers.get_cfas(db_cfas)


@cfa_router.get(path="/{cfa_token}")
def get_cfa_by_token(cfa_token: str,
                     db: Session = Depends(get_db)
                     ) -> schemas.Cfa:
    db_cfa = crud.get_cfa_by_token(db, cfa_token)

    return serializers.get_cfa(db_cfa)


@cfa_router.get(path="/history/{cfa_token}")
def get_cfa_history(cfa_token: str,
                    db: Session = Depends(get_db)
                    ) -> List[schemas.Trade]:
    db_trades = crud.get_cfa_history(db, cfa_token)
    return serializers.get_trades(db_trades)
