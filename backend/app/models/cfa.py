from typing import List

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import BaseSqlModel


class Cfa(BaseSqlModel):
    __tablename__ = 'cfas'

    token: Mapped[str] = mapped_column(String, unique=True, primary_key=True, )

    cfa_image_id: Mapped[int] = mapped_column(Integer, ForeignKey('cfa_images.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    offer_id: Mapped[int] = mapped_column(Integer, ForeignKey('offers.id'), nullable=True, default=None)

    cfa_image: Mapped['CfaImage'] = relationship('CfaImage', back_populates='cfas')
    user: Mapped['User'] = relationship(back_populates='cfas')
    offer: Mapped['Offer'] = relationship('Offer', back_populates='cfas')
    trades: Mapped[List['Trade']] = relationship('Trade', back_populates='cfa')