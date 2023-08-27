import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Cfa(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cfa'

    token = sqlalchemy.Column(sqlalchemy.String, unique=True, primary_key=True)
    cfa_image_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
