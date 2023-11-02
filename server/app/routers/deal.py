from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from requests import Session

from app import schemas, crud, serializers, errors, models, utils
from app.dependencies import get_db, current_user

deal_router = APIRouter(
    prefix="/deal",
    tags=["Deal"],
)


@deal_router.post(path="/create")
def deal_create(user: models.User = Depends(current_user),
                deal: schemas.DealCreateRequest = Body(...),
                db: Session = Depends(get_db)
                ) -> schemas.Deal:
    db_deal = crud.create_deal(db, deal, user.id)

    return serializers.get_deal(db, db_deal)


@deal_router.post(path="/cancel/{deal_id}")
def cancel_deal(deal_id: int,
                user: models.User = Depends(current_user),
                db: Session = Depends(get_db)
                ) -> Response:
    try:
        crud.unable_deal(db, user.id, deal_id)
    except errors.DealNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Response(status_code=200)


@deal_router.post(path="/accept/{deal_id}")
def accept_deal(deal_id: int,
                user: models.User = Depends(current_user),
                db: Session = Depends(get_db)
                ) -> Response:
    try:
        deal = crud.get_deal(db, deal_id)
    except errors.DealNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    host = user
    initiator = deal.initiator

    current_time = datetime.now()

    trades = []

    for cfa_image_elem in deal.initiator_items:
        cfa_image_id = cfa_image_elem['cfa_image_id']
        count = cfa_image_elem['count']
        cfas = crud.get_user_cfa_by_cfa_image(db, initiator.id, cfa_image_id, count)

        if len(cfas) < count:
            raise HTTPException(status_code=409, detail="Initiator has not enough CFA")

        for cfa in cfas:
            cfa.user_id = host.id

            trade = models.Trade(
                cfa_token=cfa.token,
                buyer_id=host.id,
                seller_id=initiator.id,
                price=0,
                created_at=current_time

            )

            trades.append(trade)

    for cfa_image_elem in deal.host_items:
        cfa_image_id = cfa_image_elem['cfa_image_id']
        count = cfa_image_elem['count']
        cfas = crud.get_user_cfa_by_cfa_image(db, host.id, cfa_image_id, count)

        if len(cfas) < count:
            raise HTTPException(status_code=409, detail="Host has not enough CFA")

        for cfa in cfas:
            cfa.user_id = initiator.id

            trade = models.Trade(
                cfa_token=cfa.token,
                buyer_id=host.id,
                seller_id=initiator.id,
                price=0,
                created_at=current_time
            )

            trades.append(trade)

    try:
        crud.accept_deal(db, user.id, deal_id)
    except errors.DealNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    crud.add_trades(db, trades)

    utils.send_email(receiver_email=initiator.email,
                     message=utils.emails.generate_message_for_initiator(initiator_name=initiator.name,
                                                                         initiator_username=initiator.username,
                                                                         host_name=host.name,
                                                                         host_username=host.username,
                                                                         date=str(current_time)))
    return Response(status_code=200)
