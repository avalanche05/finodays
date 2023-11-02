from pydantic import BaseModel
from datetime import datetime

from .user import PublicUser


class Trade(BaseModel):
    buyer: PublicUser
    cfa_token: str
    date: datetime
    id: int
    price: float
    seller: PublicUser

