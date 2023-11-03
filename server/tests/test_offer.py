from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models


def test_offer_create_get(client: TestClient, db: Session):
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

    assert response_offer_create.is_success

    db_offer = db.query(models.Offer).filter(and_(models.Offer.count == 100,
                                                  models.Offer.cfa_image_id == cfa_image_id)).first()


def test_offer_buy(client: TestClient, seller_bearer_token: str):
    seller_balance_before = \
    client.get("/user/profile", headers={"Authorization": f"Bearer {seller_bearer_token}"}).json()["balance"]
    cfa_image_id = client.post("/cfa-image/create", json={
        "count": 100,
        "description": "test cfa-image",
        "title": "test cfa-image"
    }, headers={"Authorization": f"Bearer {seller_bearer_token}"}).json()["id"]

    response_offer_create = client.post("/offer/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 100,
        "price": 100,
    }, headers={"Authorization": f"Bearer {seller_bearer_token}"}).json()

    client.post("/user/deposit", json={"value": 1000000})
    pre_user = client.get("user/profile").json()
    response = client.post(f"/offer/buy/{response_offer_create['id']}", json={"count": 100})
    assert response.is_success
    after_user = client.get("user/profile").json()
    assert pre_user["balance"] - 100 * 100 == after_user["balance"]
    seller_balance_after = \
        client.get("/user/profile", headers={"Authorization": f"Bearer {seller_bearer_token}"}).json()["balance"]
    assert seller_balance_before + 100 * 100 == seller_balance_after


def test_offer_cancel(client: TestClient, seller_bearer_token):
    cfa_image_id = client.post("/cfa-image/create", json={
        "count": 100,
        "description": "test cfa-image",
        "title": "test cfa-image"
    }).json()["id"]

    response_offer_create = client.post("/offer/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 100,
        "price": 100,
    }).json()
    user_offers = client.get(f"/offer/list/{cfa_image_id}").json()
    offer_id = user_offers[0]["id"]

    # cancel by another person
    response = client.post(f"/offer/cancel/{offer_id}", headers={"Authorization": f"Bearer {seller_bearer_token}"})
    assert not response.is_success

    # cancel by another person
    response = client.post(f"/offer/cancel/{offer_id}")
    assert response.is_success

    assert len(user_offers) - 1 == len(client.get(f"/offer/list/{cfa_image_id}").json())


def test_offer_list(client: TestClient, user_id: int):
    cfa_image_id = client.post("/cfa-image/create", json={
        "count": 111,
        "description": "test cfa-image",
        "title": "test cfa-image"
    }).json()["id"]

    response_offer_create = client.post("/offer/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 100,
        "price": 100,
    }).json()

    response_offer_create = client.post("/offer/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 10,
        "price": 10,
    }).json()

    response_offer_create = client.post("/offer/create", json={
        "cfa_image_id": cfa_image_id,
        "count": 1,
        "price": 1,
    }).json()

    offer_list_response = client.get(f"offer/list/{cfa_image_id}")

    assert offer_list_response.is_success
    assert len(offer_list_response.json()) == 3
