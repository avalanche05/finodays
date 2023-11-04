from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models


def test_desire_create(client: TestClient, db: Session, seller_bearer_token: str):
    cfa_image_id = client.post("/cfa-image/create", json={
        "count": 100,
        "description": "test cfa-image",
        "title": "test cfa-image"
    }, headers={"Authorization": f"Bearer {seller_bearer_token}"}).json()["id"]

    response_desire_create = client.post("/desire/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 100,
        "price": 100,
    })

    assert response_desire_create.is_success


def test_desire_sell(client: TestClient, seller_bearer_token: str):
    cfa_image_id = client.post("/cfa-image/create", json={
        "count": 100,
        "description": "test cfa-image",
        "title": "test cfa-image"
    }, headers={"Authorization": f"Bearer {seller_bearer_token}"}).json()["id"]

    response_desire_create = client.post("/desire/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 100,
        "price": 100,
    }).json()

    client.post("/user/deposit", json={"value": 1000000})
    pre_user = client.get("user/profile").json()

    response = client.post(f"/desire/sell/{response_desire_create['id']}",
                           headers={"Authorization": f"Bearer {seller_bearer_token}"},
                           json={"count": 100},
                           )
    assert response.is_success
    after_user = client.get("user/profile").json()
    assert pre_user["balance"] - 100 * 100 == after_user["balance"]


def test_desire_cancel(client: TestClient, seller_bearer_token):
    cfa_image_id = client.post("/cfa-image/create", json={
        "count": 100,
        "description": "test cfa-image",
        "title": "test cfa-image"
    }).json()["id"]

    response_desire_create = client.post("/desire/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 100,
        "price": 100,
    }).json()
    user_desires = client.get(f"/desire/list/{cfa_image_id}").json()
    desire_id = user_desires[0]["id"]

    # cancel by another person
    response = client.post(f"/desire/cancel/{desire_id}", headers={"Authorization": f"Bearer {seller_bearer_token}"})
    assert not response.is_success

    # cancel by another person
    response = client.post(f"/desire/cancel/{desire_id}")
    assert response.is_success

    assert len(user_desires) - 1 == len(client.get(f"/desire/list/{cfa_image_id}").json())


def test_desire_list(client: TestClient, user_id: int):
    cfa_image_id = client.post("/cfa-image/create", json={
        "count": 111,
        "description": "test cfa-image",
        "title": "test cfa-image"
    }).json()["id"]

    response_desire_create = client.post("/desire/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 100,
        "price": 100,
    }).json()

    response_desire_create = client.post("/desire/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 10,
        "price": 10,
    }).json()

    response_desire_create = client.post("/desire/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 1,
        "price": 1,
    }).json()

    desire_list_response = client.get(f"desire/list/{cfa_image_id}")

    assert desire_list_response.is_success
    assert len(desire_list_response.json()) == 3


def test_desire_autosell(client: TestClient, seller_bearer_token: str):
    cfa_image_id = client.post("/cfa-image/create", json={
        "count": 100,
        "description": "test cfa-image",
        "title": "test cfa-image"
    }).json()["id"]

    response_offer_create = client.post("/offer/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 100,
        "price": 100,
    })

    desire_offer_create = client.post("/desire/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 100,
        "price": 100,
    }, headers={"Authorization": f"Bearer {seller_bearer_token}"}).json()

    assert desire_offer_create["count"] == 0