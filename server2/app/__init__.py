from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import db, service, routers


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

    _app.include_router(routers.user.router)

    return _app
