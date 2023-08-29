import data.__all_models as db_models
from data import db_session
from openapi_server.models import PublicUser, User, CfaDTO, CfaImage
from openapi_server.models.deal_dto import DealDTO


def get_user_by_token(token: str):
    db_sess = db_session.create_session()
    token = db_sess.query(db_models.token.Token).get(token)
    if not token or not token.is_alive:
        raise Exception("Invalid credentials")
    user = db_sess.query(db_models.user.User).get(token.user_id)
    if not user:
        raise FileNotFoundError("User not found")
    return User(user.id, user.email, user.username, user.name, user.balance)


def get_public_user(user_id: int):
    db_sess = db_session.create_session()
    user = db_sess.query(db_models.user.User).get(user_id)

    if not user:
        raise FileNotFoundError("User not found")

    db_sess.close()
    return PublicUser(user.id, user.email, user.username, user.name)


def get_user(user_id: int):
    db_sess = db_session.create_session()
    user = db_sess.query(db_models.user.User).get(user_id)

    if not user:
        raise FileNotFoundError(f"Cannot find user with id {user_id}")

    db_sess.close()
    return User(user.id, user.email, user.username, user.name, user.balance)


def get_cfa(cfa_token: str):
    db_sess = db_session.create_session()
    cfa = db_sess.query(db_models.cfa.Cfa).get(cfa_token)

    if not cfa:
        raise FileNotFoundError("CFA not found")

    db_sess.close()
    return CfaDTO(cfa.token, cfa.cfa_image_id, get_public_user(cfa.user_id))


def get_cfa_image(cfa_image_id):
    db_sess = db_session.create_session()
    cfa_image = db_sess.query(db_models.cfa_image.CfaImage).get(cfa_image_id)

    if not cfa_image:
        raise FileNotFoundError("CFA Image not found")

    db_sess.close()
    return CfaImage(cfa_image.id, cfa_image.title, cfa_image.count, cfa_image.description,
                    get_public_user(cfa_image.user_id))


def get_deal(deal_id):
    db_sess = db_session.create_session()

    deal = db_sess.query(db_models.deal.Deal).filter(db_models.deal.Deal.id == deal_id).first()

    if not deal:
        raise FileNotFoundError("Deal not found")

    db_sess.close()

    return DealDTO(id=deal.id,
                   initiator=get_user(deal.initiator_id),
                   host=get_user(deal.host_id),
                   initiator_items=deal.initiator_items,
                   host_items=deal.host_items)
