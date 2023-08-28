from openapi_server.models import RegisterUserDTO, LoginUserDTO, DepositValueDTO, WithdrawValueDTO, User, PublicUser
from data import db_session
import data.__all_models as db_models
from sqlalchemy import or_
from utils import generator
from openapi_server.models import LoginResponse200


def register(register_user_dto: RegisterUserDTO):
    db_sess = db_session.create_session()

    user = db_sess.query(db_models.user.User).filter(or_(db_models.user.User.login == register_user_dto.login,
                                                         db_models.user.User.username == register_user_dto.username))

    if user.first():
        return "Invalid request", 400
    new_user = db_models.user.User()
    new_user.login = register_user_dto.login
    new_user.set_password(register_user_dto.password)
    new_user.username = register_user_dto.username
    new_user.name = register_user_dto.name
    new_user.balance = 0

    db_sess.add(new_user)
    db_sess.commit()

    token = generator.generate_bearer_token(new_user)

    db_sess.add(token)
    db_sess.commit()

    response = LoginResponse200(User(id=user.id,
                                     login=user.login,
                                     username=user.username,
                                     name=user.name,
                                     balance=user.balance), token.value)
    return response


def login(login_user_dto: LoginUserDTO):
    db_sess = db_session.create_session()

    user = db_sess.query(db_models.user.User).filter(or_(db_models.user.User.login == login_user_dto.login,
                                                         db_models.user.User.username == login_user_dto.login)).first()
    if not user:
        return "Invalid credentials", 401
    if user.check_password(login_user_dto.password):
        token = generator.generate_bearer_token(user)

        db_sess.add(token)
        db_sess.commit()

        response = LoginResponse200(User(id=user.id,
                                         login=user.login,
                                         username=user.username,
                                         name=user.name,
                                         balance=user.balance), token.value)
        return response
    return "Invalid credentials", 401


def get_cfa_list(user_id: int):
    db_sess = db_session.create_session()

    user = db_sess.query(db_models.user.User).get(user_id)
    assert user, "User not found"

    user_cfas = db_sess.query(db_models.cfa.Cfa).filter(db_models.cfa.Cfa.user_id == user_id).all()

    user_cfa_count = {}
    for cfa in user_cfas:
        user_cfa_count[cfa.cfa_image_id] = user_cfa_count.get(cfa.cfa_image_id, 0) + 1

    result = []
    for cfa_image, count in user_cfa_count.items():
        result.append({
            'cfa_image_id': cfa_image,
            'count': count
        })

    return result


def deposit_money(deposit_value_dto: DepositValueDTO, token: str):
    db_sess = db_session.create_session()

    token = db_sess.query(db_models.token.Token).get(token)
    user = db_sess.query(db_models.user.User).get(token.user_id)
    user.balance += deposit_value_dto.value

    db_sess.commit()


def withdraw_money(withdraw_value_dto: WithdrawValueDTO, token: str):
    db_sess = db_session.create_session()

    token = db_sess.query(db_models.token.Token).get(token)
    user = db_sess.query(db_models.user.User).get(token.user_id)
    user.balance -= withdraw_value_dto.value
    assert user.balance >= 0

    db_sess.commit()


def get_profile(token: str):
    db_sess = db_session.create_session()
    token = db_sess.query(db_models.token.Token).get(token)
    user = db_sess.query(db_models.user.User).get(token.user_id)

    return User(user.id, user.login, user.username, user.name, user.balance)


def get_user(user_id: int):
    db_sess = db_session.create_session()
    user = db_sess.query(db_models.user.User).get(user_id)

    assert user, "User not found"

    return PublicUser(user.id, user.login, user.username, user.name)
