from typing import List
from fastapi.testclient import TestClient
from fastapi import status
import json

import logging

import app.schemas


def test_deal_create(client: TestClient, seller_bearer_token, user_id):
    cfa_image_id = client.get(f'/user/cfa/{user_id}').json()[0]['cfa_image']['id']

    response_deal_create = client.post("/deal/create", json={
        "host_id": user_id,
        "host_items": [{
            'cfa_image_id': cfa_image_id,
            'count': 1
        }],
        "initiator_items": [{
            "cfa_image_id": 8,
            "count": 1
        }]}, headers={"Authorization": f"Bearer {seller_bearer_token}"})

    assert response_deal_create.status_code == status.HTTP_200_OK


def test_deal_accept(client: TestClient, seller_bearer_token, user_id):
    cfa_image_id = client.get(f'/user/cfa/{user_id}').json()[0]['cfa_image']['id']

    response_deal_create = client.post("/deal/create", json={
        "host_id": user_id,
        "host_items": [{
            'cfa_image_id': cfa_image_id,
            'count': 1
        }],
        "initiator_items": [{
            "cfa_image_id": 8,
            "count": 1
        }]}, headers={"Authorization": f"Bearer {seller_bearer_token}"})

    deal_id = response_deal_create.json()['id']
    response_deal_accept = client.post(f'/deal/accept/{deal_id}')

    assert 'id' in response_deal_create.json()
    assert 'initiator' in response_deal_create.json()
    assert 'host' in response_deal_create.json()
    assert 'host_items' in response_deal_create.json()
    assert 'initiator_items' in response_deal_create.json()

    assert response_deal_accept.status_code == status.HTTP_200_OK
    assert response_deal_create.status_code == status.HTTP_200_OK


def test_deal_cancel(client: TestClient, seller_bearer_token, user_id):
    cfa_image_id = client.get(f'/user/cfa/{user_id}').json()[0]['cfa_image']['id']

    response_deal_create = client.post("/deal/create", json={
        "host_id": user_id,
        "host_items": [{
            'cfa_image_id': cfa_image_id,
            'count': 1
        }],
        "initiator_items": [{
            "cfa_image_id": 8,
            "count": 1
        }]}, headers={"Authorization": f"Bearer {seller_bearer_token}"})

    deal_id = response_deal_create.json()['id']
    response_deal_cancel = client.post(f'/deal/cancel/{deal_id}')

    assert 'id' in response_deal_create.json()
    assert 'initiator' in response_deal_create.json()
    assert 'host' in response_deal_create.json()
    assert 'host_items' in response_deal_create.json()
    assert 'initiator_items' in response_deal_create.json()

    assert response_deal_cancel.status_code == status.HTTP_200_OK
    assert response_deal_create.status_code == status.HTTP_200_OK
