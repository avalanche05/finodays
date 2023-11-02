from typing import List
from fastapi.testclient import TestClient
from fastapi import status
import json

import logging

import app.schemas


def save_temp_json(file):
    json_object = json.dumps(file, indent=2)

    with open("tests/temp.json", "w") as outfile:
        outfile.write(json_object)


def test_cfa_image_create(client: TestClient):
    response = client.post('/cfa-image/create',
                           json={
                               "count": 16,
                               "description": "Artem",
                               "title": "the first cfa"
                           })

    assert response.status_code == status.HTTP_200_OK
    assert 'id' in response.json()
    assert 'count' in response.json()


def test_get_cfa_image_list(client: TestClient):
    response = client.get(f'/cfa-image/list').json()

    assert isinstance(response, list)

def test_get_cfa_image_price(client: TestClient):
    cfa_image = client.post('/cfa-image/create',
                            json={
                                "count": 16,
                                "description": "Artem",
                                "title": "the first cfa"
                            }).json()
    client.post('/offer/create', json={
        "cfa_image_id": cfa_image["id"],
        "price": 1,
        "count": 1,
    })
    client.post('/offer/create', json={
        "cfa_image_id": cfa_image["id"],
        "price": 2,
        "count": 1,
    })

    response = client.get(f'/cfa-image/price/{cfa_image["id"]}').json()

    assert 'price' in response
    assert response["price"] == 1


def test_get_cfa_image_price_history(client: TestClient, cfa_image_id: int):
    response = client.get(f'/cfa-image/price-history/{cfa_image_id}')

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert 'price' in response.json()[0]


def test_get_cfa_image_buy_advice(client: TestClient, cfa_image_id: int):
    response = client.get(f'/cfa-image/buy-advice/{cfa_image_id}')

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
    assert 'why' in response.json()
    assert 'is_buy' in response.json()



def test_get_cfa_list(client: TestClient, cfa_image_id: int):
    response = client.get(f'/cfa/list/{cfa_image_id}').json()

    assert isinstance(response, list)
    assert 'token' in response[0]
    assert 'cfa_image' in response[0]
    assert 'user' in response[0]


def test_get_history_by_token(client: TestClient):
    cfa_token = '2DgZHqRXR1DVwkejYpfb5y1CBkmDLmlBIRBpiYtpurLRAC5pAvxMeOMoD8IATye1'

    response = client.get(f'/cfa/history/{cfa_token}').json()

    assert isinstance(response, list)
    assert 'buyer' in response[0]
    assert 'cfa_token' in response[0]
    assert 'date' in response[0]
    assert 'id' in response[0]
    assert 'price' in response[0]
    assert 'seller' in response[0]


def test_get_cfa_by_token(client: TestClient, cfa_token: int):
    response = client.get(f'/cfa/{cfa_token}').json()

    assert 'token' in response
    assert 'cfa_image' in response
    assert 'user' in response
