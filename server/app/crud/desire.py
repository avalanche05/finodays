from datetime import datetime
from typing import List

from sqlalchemy.orm import Session, Mapper
from sqlalchemy import update, and_
from app import models, schemas, errors


def create_desire(db: Session, desire_create: schemas.DesireCreateRequest, user_id: int) -> models.Desire:
    db_desire = models.Desire(
        cfa_image_id=desire_create.cfa_image_id,
        count=desire_create.count,
        price=desire_create.price,
        buyer_id=user_id,
    )

    db.add(db_desire)
    db.commit()

    return db_desire


def sell_desire(db: Session, desire_sell: schemas.DesireSellRequest, desire_id: int, db_user: models.User):
    try:
        db_desire: models.Desire = db.get(models.Desire, desire_id)
    except Exception as e:
        raise errors.DesireNotFoundError(e)

    db_buyer = db_desire.buyer

    if db_buyer.balance < db_desire.price * desire_sell.count:
        raise errors.SellDesireError("Buyer has not enough money")

    if db_desire.count < desire_sell.count:
        raise errors.DesireCountNotEnough()

    current_time = datetime.now()

    trades = []
    cfas = db.query(models.Cfa).filter_by(user_id=db_user.id, offer_id=None).limit(desire_sell.count).all()

    for cfa in cfas:
        cfa.offer_id = None
        cfa.user_id = db_desire.buyer_id
        trades.append({
            'cfa_token': cfa.token,
            'price': db_desire.price,
            'buyer_id': db_desire.buyer_id,
            'seller_id': db_user.id,
            'created_at': current_time
        })

    db_desire.count -= desire_sell.count

    if db_user.id != db_buyer.id:
        db_user.sell_count += desire_sell.count
        db_user.sell_value += db_desire.price * desire_sell.count

        db_buyer.buy_count += desire_sell.count
        db_buyer.buy_value += db_desire.price * desire_sell.count

    db_user.balance += db_desire.price * desire_sell.count
    db_buyer.balance -= db_desire.price * desire_sell.count

    db.add(db_desire)
    db.add(db_user)
    db.add(db_buyer)
    db.commit()

    db.bulk_insert_mappings(models.Trade, trades)
    db.add_all(cfas)
    db.commit()


def desire_list(db: Session, cfa_image_id: int) -> List[models.Desire]:
    desires = db.query(models.Desire).filter(and_(models.Desire.cfa_image_id == cfa_image_id,
                                                  models.Desire.count > 0)).all()

    return desires


def get_user_desires(db: Session, user_id: int) -> List[models.Desire]:
    desires = db.query(models.Desire).filter(models.Desire.buyer_id == user_id, models.Desire.count > 0).all()

    return desires


def cancel_desire(db: Session, desire_id: int, db_user: models.User):
    try:
        db_desire: models.Desire = db.get(models.Desire, desire_id)
    except Exception as e:
        raise errors.DesireNotFoundError(e)

    if db_desire.buyer_id != db_user.id:
        raise errors.CancelDesireError(f"User with id {db_user.id} is not owner of desire with id {desire_id}")

    db_desire.count = 0
    db.commit()
