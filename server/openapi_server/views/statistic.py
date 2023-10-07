from data import db_session
import data.__all_models as db_models
from sqlalchemy import func


def get_statistic():
    db_sess = db_session.create_session()

    trades = db_sess.query(db_models.trade.Trade, func.count(db_models.trade.Trade.id).label('count')).group_by(db_models.trade.Trade.date).all()

    result = {
        "transactions_count": 0,
        "deals_count": 0,
        "turn": 0.0
    }

    for trade, count in trades:
        if trade.price == 0:
            result["deals_count"] += 1
        else:
            result["transactions_count"] += 1
            result["turn"] += trade.price * count

    db_sess.close()

    return result