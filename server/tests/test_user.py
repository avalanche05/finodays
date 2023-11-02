from typing import List
from fastapi.testclient import TestClient
from fastapi import status

from app.utils.token import generate_bearer_token

import app.schemas


def test_ok_register_user(client: TestClient, user_email: str, user_password: str):
    response = client.post('/user/register',
                           json={
                               "email": generate_bearer_token(),
                               "name": user_email,
                               "password": user_password,
                               "username": generate_bearer_token()
                           })
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert 'bearer_token' in response.json()
    assert 'user' in response.json()


def test_wrong_register_user(client: TestClient):
    response = client.post('/user/register',
                           json={
                               "email": "string",
                               "name": "string",
                               "password": "string",
                               "username": "string"
                           })
    assert response.status_code == status.HTTP_409_CONFLICT


def test_ok_user_login(client: TestClient):
    response = client.post('/user/login',
                           json={
                               "email": "string111",
                               "password": "string111"
                           })
    assert response.status_code == status.HTTP_200_OK


def test_ok_user_profile(client: TestClient):
    response = client.get('/user/profile')
    assert response.status_code == status.HTTP_200_OK
    assert 'balance' in response.json()
    assert 'id' in response.json()
    assert 'email' in response.json()
    assert 'name' in response.json()
    assert 'username' in response.json()


def test_ok_user_deal_in(client: TestClient):
    response = client.get('/user/deal/in')
    assert response.status_code == status.HTTP_200_OK

    deal = response.json()[0]
    assert 'id' in deal
    assert 'initiator' in deal
    assert 'host' in deal
    assert 'initiator_items' in deal
    assert 'host_items' in deal


def test_ok_deal_out(client: TestClient):
    response = client.get('user/deal/out')
    assert response.status_code == status.HTTP_200_OK

    # TODO: check the list is correct


def test_ok_get_user_by_user_id(client: TestClient):
    user_id = 1
    response = client.get(f'/user/{user_id}')
    assert response.status_code == status.HTTP_200_OK
    assert 'id' in response.json()
    assert 'email' in response.json()
    assert 'name' in response.json()
    assert 'username' in response.json()


def test_ok_get_cfa_by_user_id(client: TestClient, user_id: int):
    response = client.get(f'/user/cfa/{user_id}')
    assert response.status_code == status.HTTP_200_OK

    cfa = response.json()[0]
    assert 'cfa_image' in cfa
    assert 'count' in cfa
    assert 'tokens' in cfa


def test_ok_deposit(client: TestClient):
    response = client.post('/user/deposit', json={"value": 1})
    assert response.status_code == status.HTTP_200_OK


def test_ok_get_all_desired_by_user_id(client: TestClient):
    user_id = 1
    response = client.get(f'/user/desire/{user_id}')
    assert response.status_code == status.HTTP_200_OK

    # TODO: check the list is correct


def test_ok_get_all_offers_by_user_id(client: TestClient):
    user_id = 1
    response = client.get(f'/user/offer/{user_id}')
    assert response.status_code == status.HTTP_200_OK

    # TODO: check the list is correct


def test_ok_get_statistic_by_user_id(client: TestClient):
    user_id = 1
    response = client.get(f'/user/statistic/{user_id}')
    assert response.status_code == status.HTTP_200_OK


def test_ok_withdraw(client: TestClient):
    response = client.post('/user/withdraw',
                           json={
                               "value": 1
                           })
    assert response.status_code == status.HTTP_200_OK
