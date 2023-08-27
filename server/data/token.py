import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Token(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'token'

    value = sqlalchemy.Column(sqlalchemy.String,
                              primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user.id"))
    is_alive = sqlalchemy.Column(sqlalchemy.Boolean)
