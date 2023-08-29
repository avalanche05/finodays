from sqlalchemy import or_, and_

import data.__all_models as db_models
from data import db_session
from openapi_server.models import LoginResponse200
from openapi_server.models import RegisterUserDTO, LoginUserDTO, DepositValueDTO, WithdrawValueDTO, User, UserCfaDTO, \
    CfaImage, OfferDTO, DesireDTO
from utils import entities
from utils import generator


def register(register_user_dto: RegisterUserDTO):
    db_sess = db_session.create_session()

    user = db_sess.query(db_models.user.User).filter(or_(db_models.user.User.email == register_user_dto.email,
                                                         db_models.user.User.username == register_user_dto.username)).first()

    if user:
        db_sess.close()
        return "Invalid request", 400
    new_user = db_models.user.User()
    new_user.email = register_user_dto.email
    new_user.set_password(register_user_dto.password)
    new_user.username = register_user_dto.username
    new_user.name = register_user_dto.name
    new_user.balance = 0

    db_sess.add(new_user)
    db_sess.commit()

    token = generator.generate_bearer_token(new_user)

    db_sess.add(token)
    db_sess.commit()

    response = LoginResponse200(User(id=new_user.id,
                                     email=new_user.email,
                                     username=new_user.username,
                                     name=new_user.name,
                                     balance=new_user.balance), token.value)
    db_sess.close()
    return response


def login(login_user_dto: LoginUserDTO):
    db_sess = db_session.create_session()

    user = db_sess.query(db_models.user.User).filter(or_(db_models.user.User.email == login_user_dto.email,
                                                         db_models.user.User.username == login_user_dto.email)).first()
    if not user:
        db_sess.close()
        return "Invalid credentials", 401
    if user.check_password(login_user_dto.password):
        token = generator.generate_bearer_token(user)

        db_sess.add(token)
        db_sess.commit()

        response = LoginResponse200(User(id=user.id,
                                         email=user.email,
                                         username=user.username,
                                         name=user.name,
                                         balance=user.balance), token.value)
        db_sess.close()
        return response
    db_sess.close()
    return "Invalid credentials", 401


def get_cfa_list(user_id: int):
    db_sess = db_session.create_session()

    user_cfas = db_sess.query(db_models.cfa.Cfa).filter(
        and_(db_models.cfa.Cfa.user_id == user_id, db_models.cfa.Cfa.offer_id == 0)).all()

    user_cfa_count = {}
    for cfa in user_cfas:
        if cfa.cfa_image_id not in user_cfa_count:
            user_cfa_count[cfa.cfa_image_id] = [cfa.token]
        else:
            user_cfa_count[cfa.cfa_image_id].append(cfa.token)

    result = []
    for cfa_image_id, tokens in user_cfa_count.items():
        cfa_image = entities.get_cfa_image(cfa_image_id)
        result.append(UserCfaDTO(cfa_image, len(tokens), tokens))

    db_sess.close()
    return result


def get_offer_list(user_id: int):
    db_sess = db_session.create_session()

    user_offers = db_sess.query(db_models.offer.Offer).filter(
        and_(db_models.offer.Offer.seller_id == user_id, db_models.offer.Offer.count > 0)).all()

    result = []
    for offer in user_offers:
        result.append(OfferDTO(
            id=offer.id,
            cfa_image=entities.get_cfa_image(offer.cfa_image_id),
            count=offer.count,
            price=offer.price,
            seller=entities.get_public_user(offer.seller_id)
        ))

    db_sess.close()
    return result


def get_desire_list(user_id: int):
    db_sess = db_session.create_session()

    user_desires = db_sess.query(db_models.desire.Desire).filter(
        and_(db_models.desire.Desire.buyer_id == user_id, db_models.desire.Desire.count > 0)).all()

    result = []
    for desire in user_desires:
        try:
            cfa_image = entities.get_cfa_image(desire.cfa_image_id)
        except Exception:
            cfa_image = CfaImage(title="Cfa Not Founded")
        result.append(DesireDTO(
            id=desire.id,
            cfa_image=cfa_image,
            count=desire.count,
            price=desire.price,
            buyer=entities.get_public_user(desire.buyer_id)
        ))

    db_sess.close()
    return result


def deposit_money(deposit_value_dto: DepositValueDTO, token: str):
    db_sess = db_session.create_session()

    token = db_sess.query(db_models.token.Token).get(token)
    user = db_sess.query(db_models.user.User).get(token.user_id)
    user.balance += deposit_value_dto.value

    db_sess.commit()
    db_sess.close()


def withdraw_money(withdraw_value_dto: WithdrawValueDTO, token: str):
    db_sess = db_session.create_session()

    token = db_sess.query(db_models.token.Token).get(token)
    user = db_sess.query(db_models.user.User).get(token.user_id)
    user.balance -= withdraw_value_dto.value
    assert user.balance >= 0

    db_sess.commit()
    db_sess.close()


def get_profile(token: str):
    user = entities.get_user_by_token(token)
    return user


def get_user(user_id: int):
    user = entities.get_public_user(user_id)
    return user
