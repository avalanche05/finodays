from typing import List

from sqlalchemy import Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import BaseSqlModel
from .trade import Trade
from .deal import Deal


class User(BaseSqlModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0)
    buy_count: Mapped[int] = mapped_column(Integer, default=0)
    sell_count: Mapped[int] = mapped_column(Integer, default=0)
    buy_value: Mapped[float] = mapped_column(Float, default=0.0)
    sell_value: Mapped[float] = mapped_column(Float, default=0.0)

    cfa_images: Mapped[List['CfaImage']] = relationship(back_populates='user')
    offers: Mapped[List['Offer']] = relationship(back_populates='seller')
    cfas: Mapped[List['Cfa']] = relationship(back_populates='user')
    tokens: Mapped[List['Token']] = relationship(back_populates='user')
    as_buyer_trades: Mapped[List['Trade']] = relationship(back_populates='buyer', foreign_keys=[Trade.buyer_id])
    as_seller_trades: Mapped[List['Trade']] = relationship(back_populates='seller', foreign_keys=[Trade.seller_id])
    as_initiator_deals: Mapped[List['Deal']] = relationship(back_populates='initiator', foreign_keys=[Deal.initiator_id])
    as_host_deals: Mapped[List['Deal']] = relationship(back_populates='host', foreign_keys=[Deal.host_id])

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
