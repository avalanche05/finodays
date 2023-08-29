import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Offer(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'offer'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    cfa_image_id = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey("cfa_image.id"))
    count = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Float)
    seller_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("user.id"))
