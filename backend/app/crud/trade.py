from typing import List

from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from app import models, schemas, errors


def get_trade_by_trade_id(db: Session, trade_id: int) -> models.Trade:
    """Trade по trade_id"""

    trade = db.query(models.Trade).filter(models.Trade.id == trade_id).first()

    return trade


def get_all_trades(db: Session) -> List[models.Trade]:
    """Список всех Trade"""

    trades = db.query(models.Trade).all()

    return trades


def add_trades(db: Session, trades: List[models.Trade]):
    """Добавляет Trades"""

    db.add_all(trades)
    db.commit()


def get_user_trades(db: Session, user_id: int) -> List[models.Trade]:
    trades = db.query(models.Trade).filter(
        or_(models.Trade.seller_id == user_id,
            models.Trade.buyer_id == user_id)).all()

    return trades


def get_grouped_trades(db: Session) -> List[models.Trade]:
    trades = db.query(models.Trade.price, models.Trade.created_at).order_by(models.Trade.created_at).all()

    return trades
