import itertools
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from requests import Session

from app import schemas, crud, serializers, errors, models
from app.dependencies import get_db, current_user

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.post(path="/register")
def register_user(user: schemas.UserCreateRequest = Body(...),
                  db: Session = Depends(get_db)
                  ) -> schemas.Token:
    try:
        db_user = crud.create_user(db, user)
    except errors.EmailAlreadyAssociatedError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except errors.UsernameAlreadyAssociatedError as e:
        raise HTTPException(status_code=409, detail=str(e))
    db_token = crud.create_token(db, db_user.id)

    return serializers.get_token(db_token)


@user_router.post(path="/login")
def login_user(user: schemas.UserLoginRequest = Body(...),
               db: Session = Depends(get_db)
               ) -> schemas.Token:
    try:
        db_user = crud.read_user_by_login(db, user)
    except errors.AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    db_token = crud.create_token(db, db_user.id)

    return serializers.get_token(db_token)


@user_router.get(path="/profile")
def profile_user(user: models.User = Depends(current_user),
                 db: Session = Depends(get_db)
                 ) -> schemas.User:
    return serializers.get_user(user)


@user_router.get("/statistic")
def statistic_user(db: Session = Depends(get_db)) -> schemas.AllStatistic:
    result = schemas.AllStatistic(
        user_statistics=[]
    )

    users = crud.read_users(db)

    for user in users:
        result.user_statistics.append(
            schemas.UserStatistic(
                user=serializers.get_public_user(user),
                statistic=statistic_user_id_user(user.id, db)
            ))

    return result


@user_router.get(path="/{user_id}")
def user_id_user(user_id: int,
                 db: Session = Depends(get_db)
                 ) -> schemas.PublicUser:
    try:
        db_user = crud.read_user_by_id(db, user_id)
    except errors.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return serializers.get_public_user(db_user)


@user_router.post(path="/deposit")
def deposit_user(user: models.User = Depends(current_user),
                 deposit: schemas.UserDepositRequest = Body(...),
                 db: Session = Depends(get_db)
                 ) -> Response:
    try:
        crud.update_user_balance(db, user.id, deposit.value)
    except errors.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Response(status_code=200)


@user_router.post(path="/withdraw")
def withdraw_user(user: models.User = Depends(current_user),
                  withdraw: schemas.UserWithdrawRequest = Body(...),
                  db: Session = Depends(get_db)
                  ) -> Response:
    try:
        crud.update_user_balance(db, user.id, -withdraw.value)
    except errors.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except errors.InsufficientFundsError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Response(status_code=200)


@user_router.get("/cfa/{user_id}")
def cfa_user_id_user(user_id: int,
                     db: Session = Depends(get_db)
                     ) -> List[schemas.UserCfa]:
    try:
        user_cfas = crud.get_all_cfa_by_user_id(db, user_id)
    except errors.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    user_cfa_count = {}
    for cfa in user_cfas:
        if cfa.cfa_image_id not in user_cfa_count:
            user_cfa_count[cfa.cfa_image_id] = [cfa.token]
        else:
            user_cfa_count[cfa.cfa_image_id].append(cfa.token)

    result = []
    for cfa_image_id, tokens in user_cfa_count.items():
        try:
            cfa_image = crud.get_cfa_image(db, cfa_image_id)
            cfa_image = serializers.get_cfa_image(cfa_image)
        except errors.CfaImageNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        result.append(schemas.UserCfa(
            cfa_image=cfa_image,
            count=len(tokens),
            tokens=tokens
        ))

    return result


@user_router.get("/offer/{user_id}")
def offer_user_id_user(user_id: int,
                       db: Session = Depends(get_db)
                       ) -> List[schemas.Offer]:
    user_offers = crud.get_user_offers(db, user_id)

    try:
        user = crud.read_user_by_id(db, user_id)
        user = serializers.get_public_user(user)
    except errors.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    result = []
    for offer in user_offers:
        cfa_image = serializers.get_cfa_image(offer.cfa_image)
        result.append(schemas.Offer(
            id=offer.id,
            cfa_image=cfa_image,
            count=offer.count,
            price=offer.price,
            seller=user
        ))

    return result


@user_router.get("/desire/{user_id}")
def desire_user_id_user(user_id: int,
                        db: Session = Depends(get_db)
                        ) -> List[schemas.Desire]:
    user_desires = crud.get_user_desires(db, user_id)

    try:
        user = crud.read_user_by_id(db, user_id)
        user = serializers.get_public_user(user)
    except errors.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    result = serializers.get_desires(user_desires)

    return result


@user_router.get("/deal/in")
def deal_in_user(user: models.User = Depends(current_user),
                 db: Session = Depends(get_db)
                 ) -> List[schemas.Deal]:
    deals = crud.get_in_deals(db, user.id)

    result = serializers.get_deals(db, deals)

    return result


@user_router.get("/deal/out")
def deal_out_user(user: models.User = Depends(current_user),
                  db: Session = Depends(get_db)
                  ) -> List[schemas.Deal]:
    deals = crud.get_out_deals(db, user.id)

    result = serializers.get_deals(db, deals)

    return result


@user_router.get("/statistic/{user_id}")
def statistic_user_id_user(user_id: int,
                           db: Session = Depends(get_db)
                           ) -> schemas.Statistic:
    result = schemas.Statistic(
        transactions=schemas.TransactionsList(
            count=0,
            history=[]
        ),
        deals=schemas.DealsList(
            count=0,
            history=[]
        )
    )

    trades = crud.get_user_trades(db, user_id)

    print(1)
    trades = itertools.groupby(trades, lambda x: x.created_at)
    print(2)

    for date, grouped_trades in trades:
        grouped_trades = list(grouped_trades)
        trade = grouped_trades[0]
        count = len(grouped_trades)

        if trade.price == 0:
            result.deals.count += 1
            result.deals.history.append(schemas.StatisticDeal(
                cfa_image=trade.cfa.cfa_image_id,
                count=count,
                initiator=trade.seller_id,
                host=trade.buyer_id
            ))
        else:
            result.transactions.count += 1
            result.transactions.history.append(schemas.StatisticTransaction(
                cfa_image=trade.cfa.cfa_image_id,
                count=count,
                price=trade.price * count,
                initiator=trade.seller_id,
                host=trade.buyer_id
            ))

    print(3)

    return result
