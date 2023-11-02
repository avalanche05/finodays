from sqlalchemy import Column, Integer, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import BaseSqlModel


class Deal(BaseSqlModel):
    __tablename__ = 'deals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    initiator_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    host_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    initiator_items: Mapped[list] = mapped_column(JSON)
    host_items: Mapped[list] = mapped_column(JSON)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_accepted: Mapped[bool] = mapped_column(Boolean, default=False)

    initiator = relationship("User", foreign_keys=[initiator_id], back_populates='as_initiator_deals')
    host = relationship("User", foreign_keys=[host_id], back_populates='as_host_deals')
