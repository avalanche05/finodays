import datetime
from typing import List, Tuple

from sqlalchemy.orm import Session

from app import crud, schemas


def get_cfa_image_price_history(db: Session, cfa_image_id: int, count: int) -> Tuple[
        List[schemas.CfaImagePrice], List[schemas.CfaImagePrice], List[schemas.CfaImagePrice]]:
    offers = crud.get_offer_list(db, cfa_image_id)

    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=30)

    mins = []
    maxs = []
    latest_prices = []

    for i in range(count - 1, -1, -1):
        cur_time = now - delta * i
        min_price_for_cur_time = 1e18
        max_price_for_cur_time = -1e18
        price_of_latest_offer = None
        date_of_latest_offer = None
        for offer in offers:
            if offer.created_at <= cur_time and (
                    offer.count != 0 or offer.updated_at + delta > cur_time):
                if date_of_latest_offer is None or offer.created_at > date_of_latest_offer:
                    price_of_latest_offer = offer.price
                    date_of_latest_offer = offer.created_at
                if offer.price < min_price_for_cur_time:
                    min_price_for_cur_time = offer.price
                if offer.price > max_price_for_cur_time:
                    max_price_for_cur_time = offer.price
        if min_price_for_cur_time == 1e18:
            if mins:
                min_price_for_cur_time = mins[-1].price
            else:
                min_price_for_cur_time = 0
        if max_price_for_cur_time == -1e18:
            if maxs:
                max_price_for_cur_time = maxs[-1].price
            else:
                max_price_for_cur_time = 0
        if price_of_latest_offer is None:
            if latest_prices:
                price_of_latest_offer = latest_prices[-1].price
            else:
                price_of_latest_offer = 0
        mins.append(schemas.CfaImagePrice(
            price=min_price_for_cur_time
        ))
        maxs.append(schemas.CfaImagePrice(
            price=max_price_for_cur_time
        ))
        latest_prices.append(schemas.CfaImagePrice(
            price=price_of_latest_offer
        ))

    return mins, maxs, latest_prices
