import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Desire(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'desire'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    cfa_image_id = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey("cfa_image.id"))
    count = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Float)
    buyer_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("user.id"))
