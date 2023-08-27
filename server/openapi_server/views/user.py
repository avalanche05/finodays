from models import RegisterUserDTO
from data import db_session
from data.user import User
from data.token import Token
from sqlalchemy import or_
from utils import generator
from models import RegisterResponse200


def register(register_user_dto: RegisterUserDTO):
    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(
        or_(User.login == register_user_dto.login, User.username == register_user_dto.username))

    if user.first():
        return None, 400
    new_user = User()
    new_user.login = register_user_dto.login
    new_user.set_password(register_user_dto.password)
    new_user.username = register_user_dto.username
    new_user.name = register_user_dto.name
    new_user.balance = 0

    db_sess.add(new_user)

    token = Token()
    token.value = generator.generate_bearer_token()
    token.user_id = new_user.id
    token.is_alive = True

    db_sess.add(token)
    db_sess.commit()

    response = RegisterResponse200(new_user.id, token.value)
    return response
