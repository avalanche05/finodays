from data import db_session
from openapi_server.models.create_desire_dto import CreateDesireDTO
import data.__all_models as db_models


def create(user_id, desire_create: CreateDesireDTO):
    db_sess = db_session.create_session()

    desire = db_models.desire.Desire()
    desire.cfa_image_id = desire_create.cfa_image_id
    desire.count = desire_create.count
    desire.price = desire_create.price
    desire.buyer_id = user_id

    desire_id = desire.id
    db_sess.add(desire)
    db_sess.commit()
    db_sess.close()

    return desire_id


def cancel(user_id: int, desire_id: id):
    db_sess = db_session.create_session()

    desire = db_sess.query(db_models.desire.Desire).filter(
        db_models.desire.Desire.id == desire_id).first()

    if desire is None:
        raise FileNotFoundError(f"Cannot find desire with id {desire_id}")

    desire.count = 0

    db_sess.commit()
    db_sess.close()
