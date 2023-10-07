from data import db_session
import data.__all_models as db_models


def get_statistic():
    db_sess = db_session.create_session()

    trades = db_sess.query(db_models.trade.Trade).all()

    result = {
        "transactions_count": 0,
        "deals_count": 0,
        "turn": 0.0
    }

    for trade in trades:
        if trade.price == 0:
            result["deals_count"] += 1
        else:
            result["transactions_count"] += 1
            result["turn"] += trade.price

    db_sess.close()

    return result