from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import BaseSqlModel


class Trade(BaseSqlModel):
    __tablename__ = 'trades'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cfa_token: Mapped[str] = mapped_column(String, ForeignKey('cfas.token'))
    price: Mapped[float] = mapped_column(Float)
    buyer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    cfa = relationship('Cfa', back_populates='trades')
    buyer = relationship('User', foreign_keys=[buyer_id], back_populates='as_buyer_trades')
    seller = relationship('User', foreign_keys=[seller_id], back_populates='as_seller_trades')
