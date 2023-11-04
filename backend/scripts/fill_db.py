from app import models
from app import dependencies
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, Session


def fill_db():
    db = next(dependencies.get_db())

    for t in db.query(models.Offer).all():
        print(t.__dict__)


fill_db()
