import datetime
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
    cfas = crud.get_all_cfa(db)

    trades = itertools.groupby(trades, lambda x: x[1])

    current_time = datetime.datetime.now()
    fix_timezone = datetime.timedelta(hours=3)
    one_hour = datetime.timedelta(hours=1)

    new_cfas = [cfa for cfa in cfas if cfa.created_at + fix_timezone + one_hour >= current_time]

    result = schemas.CountStatistic(
        transactions_count=0,
        transactions_count_increment=0,
        deals_count=0,
        deals_count_increment=0,
        turn=0.0,
        turn_increment=0.0,
        created_cfa_count=len(cfas),
        created_cfa_count_increment=len(new_cfas)
    )

    for date, grouped_trades in trades:
        grouped_trades = list(grouped_trades)
        trade = grouped_trades[0]
        if trade.price == 0:
            result.deals_count += 1
            if date + one_hour >= current_time:
                result.deals_count_increment += 1
        else:
            result.transactions_count += 1
            result.turn += trade.price * len(grouped_trades)
            if date + one_hour >= current_time:
                result.transactions_count_increment += 1
                result.turn_increment += trade.price * len(grouped_trades)

    return result


@statistic_router.get(path="/score")
def get_score(sort_by: str = Query("count", description="Sort type"),
              limit: int = Query(None, description="Number of users to return"),
              db: Session = Depends(get_db)) -> List[schemas.StatisticUser]:
    db_users = crud.get_user_statistic(db, sort_by, limit)

    return serializers.get_statistic_users(db_users)
