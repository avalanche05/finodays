from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import db
from app import routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    db.BaseSqlModel.metadata.create_all(bind=db.engine)
    yield


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(routers.user.user_router)
    _app.include_router(routers.cfa_image.cfa_image_router)
    _app.include_router(routers.cfa.cfa_router)
    _app.include_router(routers.offer.offer_router)
    _app.include_router(routers.desire.desire_router)
    _app.include_router(routers.deal.deal_router)
    _app.include_router(routers.statistic.statistic_router)
    _app.include_router(routers.trade.trade_router)

    return _app
