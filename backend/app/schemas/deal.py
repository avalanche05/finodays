from typing import List
from pydantic import BaseModel

from .cfa_image import CfaImage
from .user import PublicUser


class Deal(BaseModel):
    id: int
    initiator: PublicUser
    host: PublicUser
    initiator_items: List
    host_items: List


class DealCreateRequest(BaseModel):
    initiator_items: List
    host_items: List
    host_id: int


class StatisticDeal(BaseModel):
    cfa_image: int
    count: int
    initiator: int
    host: int


class DealsList(BaseModel):
    count: int
    history: List[StatisticDeal]
