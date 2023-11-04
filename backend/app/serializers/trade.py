from typing import List

from app import models, schemas
from .user import get_public_user


def get_trade(db_trade: models.Trade) -> schemas.Trade:
    trade = schemas.Trade(
        buyer=get_public_user(db_trade.buyer),
        cfa_token=db_trade.cfa_token,
        date=db_trade.created_at,
        id=db_trade.id,
        price=db_trade.price,
        seller=get_public_user(db_trade.seller)
    )

    return trade


def get_trades(db_trades: List[models.Trade]) -> List[schemas.Trade]:
    return [get_trade(db_trade) for db_trade in db_trades]
