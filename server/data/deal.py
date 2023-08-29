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
    initiator_items = sqlalchemy.Column(sqlalchemy.JSON)
    host_items = sqlalchemy.Column(sqlalchemy.JSON)
