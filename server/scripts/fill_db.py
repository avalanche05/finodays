import json

from app import models
from app import dependencies
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from requests import Session

HOST = "https://api.misis-gis.ru"


def url(path: str):
    return HOST + "/" + path


def get_seller_id(seller_ticker: str):
    with open("seller_id.json") as seller_id_file:
        seller_id_json = dict(json.load(seller_id_file))

        return seller_id_json.get(seller_ticker, None)


def create_seller(seller_ticker: str, session: Session):
    session.post(url("/"))


def mock_price_history():
    pass
