import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Deal(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'deal'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    initiator_id = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey("user.id"))
    host_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user.id"))
    initiator_items = sqlalchemy.Column(sqlalchemy.JSON)
    host_items = sqlalchemy.Column(sqlalchemy.JSON)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=sqlalchemy.True_)
    is_accepted = sqlalchemy.Column(sqlalchemy.Boolean, default=sqlalchemy.False_)

