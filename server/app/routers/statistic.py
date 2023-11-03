import itertools
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Response, Query
from requests import Session

from app import schemas, crud, serializers, errors, models
from app.dependencies import get_db, current_user

statistic_router = APIRouter(
    prefix="/statistic",
    tags=["Statistic"],
)


@statistic_router.get(path="/")
def statistic(db: Session = Depends(get_db)) -> schemas.CountStatistic:
    trades = crud.get_grouped_trades(db)

    trades = itertools.groupby(trades, lambda x: x[1])

    result = schemas.CountStatistic(
        transactions_count=0,
        deals_count=0,
        turn=0.0
    )

    for date, grouped_trades in trades:
        grouped_trades = list(grouped_trades)
        trade = grouped_trades[0]
        if trade.price == 0:
            result.deals_count += 1
        else:
            result.transactions_count += 1
            result.turn += trade.price * len(grouped_trades)

    return result


@statistic_router.get(path="/score")
def get_score(sort_by: str = Query("count", description="Sort type"),
              limit: int = Query(None, description="Number of users to return"),
              db: Session = Depends(get_db)) -> List[schemas.StatisticUser]:
    db_users = crud.get_user_statistic(db, sort_by, limit)

    return serializers.get_statistic_users(db_users)
