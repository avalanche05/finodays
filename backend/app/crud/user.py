from sqlalchemy.orm import Session
from app import models, schemas, errors
from .token import read_token


def create_user(db: Session, payload: schemas.UserCreateRequest) -> models.User:
    """Создание пользователя"""

    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if user is not None:
        raise errors.EmailAlreadyAssociatedError()

    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if user is not None:
        raise errors.UsernameAlreadyAssociatedError()

    db_user = models.User(
        email=payload.email,
        username=payload.username,
        name=payload.name,
    )
    db_user.set_password(payload.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def read_user_by_login(db: Session, payload: schemas.UserLoginRequest) -> models.User:
    """Получение пользователя"""
    user = db.query(models.User).filter(models.User.email == payload.email).first()

    if user is None:
        raise errors.AuthenticationError()

    if user.check_password(payload.password):
        return user

    raise errors.AuthenticationError()


def read_user_by_id(db: Session, user_id: int) -> models.User:
    """Получение пользователя"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise errors.UserNotFoundError()

    return user


def read_user_by_token(db: Session, token: str) -> models.User:
    """Получение пользователя"""
    token = read_token(db, token)

    user = db.query(models.User).filter(models.User.id == token.user_id).first()

    if user is None:
        raise errors.UserNotFoundError()

    return user


def update_user_balance(db: Session, user_id: int, value):
    """Обновления баланса"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise errors.UserNotFoundError()

    if user.balance + value < 0:
        raise errors.InsufficientFundsError()

    user.balance += value

    db.commit()
    db.refresh(user)


def read_users(db: Session):
    """Получение всех пользователей"""
    users = db.query(models.User).all()

    return users
