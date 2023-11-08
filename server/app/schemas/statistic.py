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
    transactions_count_increment: int
    deals_count: int
    deals_count_increment: int
    turn: float
    turn_increment: float
    created_cfa_count: int
    created_cfa_count_increment: int


class AllStatistic(BaseModel):
    user_statistics: List[UserStatistic]
