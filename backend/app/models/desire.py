from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import BaseSqlModel


class Desire(BaseSqlModel):
    __tablename__ = 'desires'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    cfa_image_id: int = Column(Integer, ForeignKey("cfa_images.id"))
    count: int = Column(Integer)
    # price: float = Column(Float)
    price: Mapped[float] = mapped_column(Float)
    buyer_id: int = Column(Integer, ForeignKey("users.id"))

    cfa_image = relationship("CfaImage")
    buyer = relationship("User")
