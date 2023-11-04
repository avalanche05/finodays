from app.models import user as db_model_user
from app import schemas


def get_user(db_user: db_model_user.User) -> schemas.User:
    user = schemas.User(
        id=db_user.id,
        email=db_user.email,
        username=db_user.username,
        name=db_user.name,
        balance=db_user.balance,
    )

    return user


def get_public_user(db_user: db_model_user.User) -> schemas.PublicUser:
    user = schemas.PublicUser(
        id=db_user.id,
        email=db_user.email,
        username=db_user.username,
        name=db_user.name
    )

    return user
