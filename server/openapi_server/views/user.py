from openapi_server.models import RegisterUserDTO, LoginUserDTO
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

    response = LoginResponse200(new_user.id, token.value)
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

        response = LoginResponse200(user.id, token.value)
        return response
    return "Invalid credentials", 401
