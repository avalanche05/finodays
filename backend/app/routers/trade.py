from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from requests import Session

from app import schemas, crud, serializers, models
from app.dependencies import get_db, current_user

trade_router = APIRouter(
    prefix="/trade",
    tags=["Trade"],
)


@trade_router.get(path='/list')
def trade_list(db: Session = Depends(get_db)) -> List[schemas.Trade]:
    db_trades = crud.get_all_trades(db)

    return serializers.get_trades(db_trades)


@trade_router.get(path='/{trade_id}')
def get_trade_by_trade_id(trade_id: int,
                          db: Session = Depends(get_db)
                          ) -> schemas.Trade:
    db_trade_by_trade_id = crud.get_trade_by_trade_id(db, trade_id)

    return serializers.get_trade(db_trade_by_trade_id)
