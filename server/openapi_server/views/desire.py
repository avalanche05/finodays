from datetime import datetime

from sqlalchemy import desc

from data import db_session
import data.__all_models as db_models
from utils import entities
from openapi_server.models.create_desire_dto import CreateDesireDTO
from openapi_server.models.desire_dto import DesireDTO


def get_all_by_cfa_image_id(cfa_image_id: int):
    db_sess = db_session.create_session()

    desires = db_sess.query(db_models.desire.Desire).filter(
        db_models.desire.Desire.cfa_image_id == cfa_image_id, db_models.desire.Desire.count > 0) \
        .order_by(desc(db_models.desire.Desire.price)).all()

    result = []
    for desire in desires:
        result.append(
            DesireDTO(
                id=desire.id,
                cfa_image=entities.get_cfa_image(desire.cfa_image_id),
                count=desire.count,
                price=desire.price,
                buyer=entities.get_public_user(desire.buyer_id)
            )
        )
    db_sess.close()
    return result


def sell(desire_id: int, user_id: int, count: int):
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


def create(user_id, desire_create: CreateDesireDTO):
    db_sess = db_session.create_session()

    cfa_image = db_sess.query(db_models.cfa_image.CfaImage).filter(
        db_models.cfa_image.CfaImage.id == desire_create.cfa_image_id).first()

    if cfa_image is None:
        raise ValueError(f"CfaImage with id: {desire_create.cfa_image_id} not exist")

    if desire_create.count <= 0:
        raise ValueError("Count should be positive")

    if desire_create.count > cfa_image.count:
        raise ValueError(f"Marketplace have only {cfa_image.count} CFAs, it is unreal to buy {desire_create.count}")

    desire = db_models.desire.Desire()
    desire.cfa_image_id = desire_create.cfa_image_id
    desire.count = desire_create.count
    desire.price = desire_create.price
    desire.buyer_id = user_id

    db_sess.add(desire)
    db_sess.commit()
    desire_id = desire.id

    offers = db_sess.query(db_models.offer.Offer).filter(
        db_models.offer.Offer.cfa_image_id == desire.cfa_image_id,
        db_models.offer.Offer.count > 0,
        db_models.offer.Offer.price <= desire.price,
        db_models.offer.Offer.seller_id != desire.buyer_id
    ).all()

    bought_count = 0
    for offer in offers:
        count = min(desire.count - bought_count, offer.count)
        try:
            sell(desire_id, offer.seller_id, count)
            bought_count += count
        except Exception:
            pass

        if bought_count == offer.count:
            break

    db_sess.close()

    return desire_id


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
