from typing import List

from sqlalchemy.orm import Session

from app.models import deal as db_model_deal
from app import schemas, serializers, crud

from .user import get_user


def get_deal(db: Session, db_deal: db_model_deal.Deal) -> schemas.Deal:
    deal = schemas.Deal(
        id=db_deal.id,
        initiator=serializers.get_public_user(db_deal.initiator),
        host=serializers.get_public_user(db_deal.host),
        initiator_items=get_deal_items(db, db_deal.initiator_items),
        host_items=get_deal_items(db, db_deal.host_items)
    )

    return deal


def get_deals(db: Session, db_deals: List[db_model_deal.Deal]) -> List[schemas.Deal]:
    deals = [get_deal(db, db_deal) for db_deal in db_deals]
    return deals


def get_deal_items(db: Session, items: List):
    result = []
    for item in items:
        cfa_image = crud.get_cfa_image(db, item["cfa_image_id"])
        cfa_image = serializers.get_cfa_image(cfa_image)
        result.append({
            "count": item["count"],
            "cfa_image": cfa_image
        })
    return result
