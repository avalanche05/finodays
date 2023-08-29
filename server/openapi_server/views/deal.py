from datetime import datetime

from sqlalchemy import desc

from data import db_session
import data.__all_models as db_models
from openapi_server.models.deal_dto import DealDTO
from utils import entities
from openapi_server.models.create_deal_dto import CreateDealDTO
from openapi_server.models.desire_dto import DesireDTO


def accept(deal_id: int, user_id: int, count: int):
    db_sess = db_session.create_session()

    desire = db_sess.query(db_models.desire.Desire).filter(
        db_models.desire.Desire.id == desire_id).first()

    if desire is None:
        raise FileNotFoundError(f"Cannot find offer with id {desire}")

    if count < 0 or count > desire.count:
        raise ValueError("Wrong count value")

    if desire.buyer_id == user_id:
        raise ValueError("You cannot sell desires from yourself")

    user = db_sess.query(db_models.user.User).get(user_id)
    buyer = db_sess.query(db_models.user.User).get(desire.buyer_id)

    if user is None:
        raise FileNotFoundError(f"Cannot find user with id {user_id}")
    if buyer is None:
        raise FileNotFoundError(f"Cannot find user with id {desire.buyer_id}")

    calculated_price = desire.price * count

    if calculated_price > buyer.balance:
        raise ValueError("Buyer have not enough money")

    buyer.balance -= calculated_price
    desire.count -= count

    cfas = db_sess.query(db_models.cfa.Cfa).filter(
        db_models.cfa.Cfa.user_id == user_id,
        db_models.cfa.Cfa.cfa_image_id == desire.cfa_image_id,
    ).limit(count).all()

    if len(cfas) < count:
        raise ValueError("User have not enough CFA")

    user.balance += calculated_price

    for cfa in cfas:
        cfa.user_id = buyer.id

        trade = db_models.trade.Trade()
        trade.date = datetime.now()
        trade.cfa_token = cfa.token
        trade.price = desire.price
        trade.buyer_id = desire.buyer_id
        trade.seller_id = user_id

        db_sess.add(trade)

    db_sess.commit()
    db_sess.close()


def create(initiator_id, create_deal: CreateDealDTO):
    db_sess = db_session.create_session()

    deal = db_models.deal.Deal()
    deal.initiator_id = initiator_id
    deal.host_id = create_deal.host_id
    deal.initiator_items = create_deal.initiator_items
    deal.host_items = create_deal.host_items
    deal.is_active = True
    deal.is_accepted = False

    db_sess.add(deal)
    db_sess.commit()
    deal_id = deal.id
    db_sess.close()

    return deal_id


def cancel(user_id: int, desire_id: id):
    db_sess = db_session.create_session()

    desire = db_sess.query(db_models.desire.Desire).filter(
        db_models.desire.Desire.id == desire_id).first()

    if desire is None:
        raise FileNotFoundError(f"Cannot find desire with id: {desire_id}")

    if desire.buyer_id != user_id:
        raise ValueError(f"You cannot cancel desire with id: {desire_id}")

    desire.count = 0

    db_sess.commit()
    db_sess.close()


def get_all_in_deals(user_id: int):
    db_sess = db_session.create_session()

    deals = db_sess.query(db_models.deal.Deal).filter(
        db_models.deal.Deal.host_id == user_id,
        db_models.deal.Deal.is_active == True).all()

    result = []
    for deal in deals:
        result.append(
            DealDTO()
        )


