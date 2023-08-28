import data.__all_models as db_models
from data import db_session
from openapi_server.models.trade_dto import TradeDTO
import openapi_server.views as views


def get_all():
    db_sess = db_session.create_session()

    trades = db_sess.query(db_models.trade.Trade).all()
    result = []
    for trade in trades:
        result.append(
            TradeDTO(
                id=trade.id,
                date=trade.date,
                cfa_token=trade.cfa_token,
                price=trade.price,
                buyer=views.user.get_user(trade.buyer_id),
                seller=views.user.get_user(trade.seller_id)
            )
        )

    return result


def get_by_id(trade_id: int):
    db_sess = db_session.create_session()

    trade = db_sess.query(db_models.trade.Trade).filter(
        db_models.trade.Trade.id == trade_id
    ).first()

    trade_dto = TradeDTO(
        id=trade.id,
        date=trade.date,
        cfa_token=trade.cfa_token,
        price=trade.price,
        buyer=views.user.get_user(trade.buyer_id),
        seller=views.user.get_user(trade.seller_id)
    )

    return trade_dto
