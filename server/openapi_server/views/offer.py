from datetime import datetime

from data import db_session
from openapi_server.models.create_offer_dto import CreateOfferDTO
from openapi_server.models.offer_dto import OfferDTO
import data.__all_models as db_models
from utils import entities, email


def create(user_id, offer_create: CreateOfferDTO):
    db_sess = db_session.create_session()

    cfas = db_sess.query(db_models.cfa.Cfa).filter(
        db_models.cfa.Cfa.user_id == user_id,
        db_models.cfa.Cfa.cfa_image_id == offer_create.cfa_image_id,
        db_models.cfa.Cfa.offer_id == 0
    ).all()

    if offer_create.count <= 0:
        raise ValueError("Count should be positive")

    if offer_create.count > len(cfas):
        db_sess.close()
        raise ValueError("User have not enough cfas to sell")

    offer = db_models.offer.Offer()
    offer.seller_id = user_id
    offer.price = offer_create.price
    offer.cfa_image_id = offer_create.cfa_image_id
    offer.count = offer_create.count
    db_sess.add(offer)
    db_sess.commit()

    for i in range(offer_create.count):
        cfas[i].offer_id = offer.id

    offer_id = offer.id

    db_sess.commit()

    # Проверяем существуют ли заявки на покупку которым удовлетворяет созданное предложение

    desires = db_sess.query(db_models.desire.Desire).filter(
        db_models.desire.Desire.count > 0,
        db_models.desire.Desire.buyer_id != offer.seller_id,
        db_models.desire.Desire.cfa_image_id == offer.cfa_image_id,
        db_models.desire.Desire.price >= offer.price
    ).all()

    selled_count = 0
    for desire in desires:
        count = min(desire.count, offer.count - selled_count)
        try:
            buy(offer.id, desire.buyer_id, count)
            selled_count += count
        except Exception:
            pass

        if selled_count == offer.count:
            break

    db_sess.close()

    return offer_id


def cancel_offer(user_id: int, offer_id: id):
    db_sess = db_session.create_session()

    offer = db_sess.query(db_models.offer.Offer).filter(
        db_models.offer.Offer.id == offer_id).first()

    if offer is None:
        raise FileNotFoundError(f"Cannot find offer with id: {offer_id}")

    if user_id != offer.seller_id:
        raise ValueError(f"You cannot cancel offer with id: {offer_id}")

    cfas = db_sess.query(db_models.cfa.Cfa).filter(
        db_models.cfa.Cfa.user_id == user_id,
        db_models.cfa.Cfa.cfa_image_id == offer.cfa_image_id,
        db_models.cfa.Cfa.offer_id == offer_id
    ).all()

    for cfa in cfas:
        cfa.offer_id = 0
        db_sess.commit()

    offer.count = 0

    db_sess.commit()
    db_sess.close()


def get_all_by_cfa_image_id(cfa_image_id: int):
    db_sess = db_session.create_session()

    offers = db_sess.query(db_models.offer.Offer).filter(
        db_models.offer.Offer.cfa_image_id == cfa_image_id, db_models.offer.Offer.count > 0) \
        .order_by(db_models.offer.Offer.price).all()

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

    if offer.seller_id == user_id:
        raise ValueError("You cannot buy offers from yourself")

    user = db_sess.query(db_models.user.User).filter(
        db_models.user.User.id == user_id).first()

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
        db_models.user.User.id == offer.seller_id).first()
    seller.balance += calculated_price

    current_time = datetime.now()

    for cfa in cfas:
        cfa.user_id = user_id
        cfa.offer_id = 0

        trade = db_models.trade.Trade()
        trade.date = current_time
        trade.cfa_token = cfa.token
        trade.price = offer.price
        trade.buyer_id = user_id
        trade.seller_id = offer.seller_id

        db_sess.add(trade)
        db_sess.commit()

    try:
        email.send_email(receiver_email=seller.email,
                     message=email.generate_message_for_seller(seller_name=seller.name,
                                                               seller_username=seller.username,
                                                               buyer_name=user.name,
                                                               buyer_username=user.username,
                                                               date=str(current_time),
                                                               amount=calculated_price))
    except Exception as e:
        pass

    db_sess.commit()
    db_sess.close()
