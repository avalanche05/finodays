from typing import List

from pydantic import BaseModel
from .deal import DealsList
from .user import PublicUser
from .cfa_image import CfaImage



class StatisticTransaction(BaseModel):
    cfa_image: int
    count: int
    price: float
    initiator: int
    host: int


class TransactionsList(BaseModel):
    count: int
    history: List[StatisticTransaction]


class Statistic(BaseModel):
    transactions: TransactionsList
    deals: DealsList


class UserStatistic(BaseModel):
    user: PublicUser
    statistic: Statistic


class CountStatistic(BaseModel):
    transactions_count: int
    deals_count: int
    turn: float


class AllStatistic(BaseModel):
    user_statistics: List[UserStatistic]
