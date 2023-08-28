from data import db_session
from models import User
from openapi_server.models import CfaDTO
from openapi_server.models import TradeDTO
from utils import generator
import data.__all_models as db_models
import openapi_server.views as views
import openapi_server.views as views
from utils import entities


def create_cfa(user_id: int, cfa_image_id: int):
    token = generator.generate_cfa_token()

    cfa = db_models.cfa.Cfa()
    cfa.user_id = user_id
    cfa.cfa_image_id = cfa_image_id
    cfa.token = token

    db_sess = db_session.create_session()
    db_sess.add(cfa)
    db_sess.commit()


def get_cfa(cfa_token: str):
    cfa = entities.get_cfa(cfa_token)
    return cfa


def get_cfa_history(cfa_token: str):
    db_sess = db_session.create_session()

    trades = db_sess.query(db_models.trade.Trade).filter(db_models.trade.Trade.cfa_token == cfa_token).order_by(
        db_models.trade.Trade.date).all()

    history = []

    for trade in trades:
        history.append(TradeDTO(
            id=trade.id,
            date=trade.date,
            cfa_token=trade.cfa_token,
            price=trade.price,
            buyer=entities.get_public_user(trade.buyer_id),
            seller=entities.get_public_user(trade.seller_id)
        ))

    if history:
        return history, 200
    else:
        return "CFA not found", 404


def get_cfa_list(cfa_image_id: int):
    db_sess = db_session.create_session()

    cfa_list = db_sess.query(db_models.cfa.Cfa).filter(db_models.cfa.Cfa.cfa_image_id == cfa_image_id).all()

    db_sess.close()
    assert cfa_list, "CFA Image not found"

    result = []
    users = {}
    for cfa in cfa_list:
        if cfa.user_id in users:
            user = users[cfa.user_id]
        else:
            try:
                user = entities.get_public_user(cfa.user_id)
            except Exception:
                user = User(username="User Not Founded")
        result.append(CfaDTO(
            token=cfa.token,
            cfa_image_id=cfa.cfa_image_id,
            user=user
        ))
        print(len(result))
    return result
