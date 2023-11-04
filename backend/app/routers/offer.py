from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status, Response
from requests import Session

from app import schemas, crud, serializers, models, errors
from app.dependencies import get_db, current_user

offer_router = APIRouter(
    prefix="/offer",
    tags=["Offer"],
)


@offer_router.post(path="/create")
def offer_create(create_offer: schemas.OfferCreateRequest = Body(...),
                 user: models.User = Depends(current_user),
                 db: Session = Depends(get_db)
                 ) -> schemas.Offer:
    if create_offer.count <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Count must be positive")
    db_offer = crud.create_offer(db, create_offer, user.id)

    desires = crud.get_cfa_image_desires_with_greater_price(db, create_offer.cfa_image_id, create_offer.price, user.id)

    sold_count = 0
    for desire in desires:
        count = min(desire.count, create_offer.count - sold_count)
        offer_buy = schemas.OfferBuyRequest(
            count=count
        )
        try:
            crud.buy_offer(db, offer_buy, db_offer.id, desire.buyer)
            sold_count += count
        except Exception:
            pass

        if sold_count == db_offer.count:
            break

    db.refresh(db_offer)

    return serializers.get_offer(db_offer)


@offer_router.post(path="/buy/{offer_id}")
def buy_offer(offer_id: int,
              offer_buy: schemas.OfferBuyRequest,
              user: models.User = Depends(current_user),
              db: Session = Depends(get_db),
              ):

    try:
        crud.buy_offer(db, offer_buy, offer_id, user)
    except errors.OfferNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.message)
    except errors.BuyOfferError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)
    except errors.OfferCountNotEnough as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)


@offer_router.get(path="/list/{cfa_image_id}")
def offer_list(cfa_image_id: int,
               db: Session = Depends(get_db),
               ) -> List[schemas.Offer]:
    db_offers = crud.get_active_offer_list(db, cfa_image_id)

    return serializers.get_offers(db_offers)


@offer_router.post(path="/cancel/{offer_id}")
def offer_cancel(offer_id: int,
                 user: models.User = Depends(current_user),
                 db: Session = Depends(get_db),
                 ):
    try:
        crud.cancel_offer(db, offer_id, user)
    except errors.CancelOfferError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)
    except errors.OfferNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Offer with id {offer_id} not found")

    return Response(status_code=status.HTTP_200_OK)
