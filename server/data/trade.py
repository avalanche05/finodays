import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Trade(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'trade'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True),
                             server_default=sqlalchemy.sql.func.now())
    cfa_token = sqlalchemy.Column(sqlalchemy.String,
                                  sqlalchemy.ForeignKey("cfa.token"))
    price = sqlalchemy.Column(sqlalchemy.Float)
    buyer_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("user.id"))
    seller_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("user.id"))

