from datetime import datetime

from data import db_session
from openapi_server.models.create_offer_dto import CreateOfferDTO
from openapi_server.models.offer_dto import OfferDTO
import data.__all_models as db_models
from utils import entities

def create(user_id, offer_create: CreateOfferDTO):
    db_sess = db_session.create_session()

    cfas = db_sess.query(db_models.cfa.Cfa).filter(
        db_models.cfa.Cfa.user_id == user_id,
        db_models.cfa.Cfa.cfa_image_id == offer_create.cfa_image_id,
        db_models.cfa.Cfa.offer_id == 0
    ).all()

    if offer_create.count > len(cfas):
        raise ValueError("User have not enough cfas to sell")

    offer = db_models.offer.Offer()
    offer.seller_id = user_id
    offer.price = offer_create.price
    offer.cfa_image_id = offer_create.cfa_image_id
    offer.count = offer_create.count

    for i in range(offer_create.count):
        cfas[i].offer_id = offer.id

    db_sess.add(offer)
    db_sess.commit()
    db_sess.close()

    return offer.id

def cancel_offer(user_id: int, offer_id: id):
    db_sess = db_session.create_session()

    offer = db_sess.query(db_models.offer.Offer).filter(
        db_models.offer.Offer.id == offer_id).first()

    if offer is None:
        raise FileNotFoundError(f"Cannot find offer with id {offer_id}")

    cfas = db_sess.query(db_models.cfa.Cfa).filter(
        db_models.cfa.Cfa.user_id == user_id,
        db_models.cfa.Cfa.cfa_image_id == offer.cfa_image_id,
        db_models.cfa.Cfa.offer_id == offer_id
    ).all()

    for cfa in cfas:
        cfa.offer_id = 0

    offer.count = 0

    db_sess.close()
    db_sess.commit()


def get_all_by_cfa_image_id(cfa_image_id: int):
    db_sess = db_session.create_session()

    offers = db_sess.query(db_models.offer.Offer).filter(
        db_models.offer.Offer.cfa_image_id == cfa_image_id, db_models.offer.Offer.count > 0).all()

    result = []
    for offer in offers:
        result.append(
            OfferDTO(
                id=offer.id,
                cfa_image=entities.get_cfa_image(offer.cfa_image_id),
                count=offer.count,
                price=offer.price,
                seller=entities.get_public_user(offer.seller_id)
            )
        )
    db_sess.close()
    return result


def buy(offer_id: int, user_id: int, count: int):
    db_sess = db_session.create_session()

    offer = db_sess.query(db_models.offer.Offer).filter(
        db_models.offer.Offer.id == offer_id).first()

    if offer is None:
        raise FileNotFoundError(f"Cannot find offer with id {offer_id}")

    if count < 0 or count > offer.count:
        raise ValueError("Wrong count value")

    user = db_sess.query(db_models.user.User).filter(
        db_models.user.User.id == user_id
    ).first()

    if user is None:
        raise FileNotFoundError(f"Cannot find user with id {user_id}")

    calculated_price = offer.price * count

    if calculated_price > user.balance:
        raise ValueError("User have not enough money")

    user.balance -= calculated_price
    offer.count -= count

    cfas = db_sess.query(db_models.cfa.Cfa).filter(
        db_models.cfa.Cfa.user_id == offer.seller_id,
        db_models.cfa.Cfa.cfa_image_id == offer.cfa_image_id,
        db_models.cfa.Cfa.offer_id == offer.id
    ).limit(count).all()

    seller = db_sess.query(db_models.user.User).filter(
        db_models.user.User.id == offer.seller_id
    ).first()
    seller.balance += calculated_price

    for cfa in cfas:
        cfa.user_id = user_id

        trade = db_models.trade.Trade()
        trade.date = datetime.now()
        trade.cfa_token = cfa.token
        trade.price = offer.price
        trade.buyer_id = user_id
        trade.seller_id = offer.seller_id

        db_sess.add(trade)

    db_sess.commit()
    db_sess.close()