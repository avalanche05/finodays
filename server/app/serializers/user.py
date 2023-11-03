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


def get_statistic_user(db_user: db_model_user.User) -> schemas.StatisticUser:
    user = schemas.StatisticUser(
        id=db_user.id,
        email=db_user.email,
        username=db_user.username,
        name=db_user.name,
        buy_count=db_user.buy_count,
        buy_value=db_user.buy_value,
        sell_count=db_user.sell_count,
        sell_value=db_user.sell_value,
    )

    return user


def get_statistic_users(db_users: list[db_model_user.User]) -> list[schemas.StatisticUser]:
    return [get_statistic_user(db_user) for db_user in db_users]
