from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import BaseSqlModel


class CfaImage(BaseSqlModel):
    __tablename__ = 'cfa_images'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    count: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user: Mapped['User'] = relationship(back_populates='cfa_images')
    offers = relationship('Offer', back_populates='cfa_image')
    cfas = relationship('Cfa', back_populates='cfa_image')
