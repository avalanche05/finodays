from typing import List
from fastapi.testclient import TestClient
from fastapi import status
import json

import logging

import app.schemas


def test_trade_list(client: TestClient):
    response = client.get(f'/trade/list')

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert 'buyer' in response.json()[0]
    assert 'seller' in response.json()[0]
    assert 'cfa_token' in response.json()[0]
    assert 'date' in response.json()[0]
    assert 'id' in response.json()[0]
    assert 'price' in response.json()[0]


def test_trade_by_id(client: TestClient):
    response_list = client.get(f'/trade/list')
    trade_id = response_list.json()[0]['id']

    response = client.get(f'/trade/{trade_id}')

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
