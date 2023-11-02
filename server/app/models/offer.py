from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import BaseSqlModel


class Offer(BaseSqlModel):
    __tablename__ = 'offers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cfa_image_id: Mapped[int] = mapped_column(Integer, ForeignKey('cfa_images.id'))
    count: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    cfa_image = relationship('CfaImage', back_populates='offers')
    seller: Mapped['User'] = relationship(back_populates='offers')
    cfas = relationship('Cfa', back_populates='offer')
