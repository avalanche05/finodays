import pytest
from fastapi.testclient import TestClient
from requests import Session

from app.main import app
from app.dependencies import get_db


@pytest.fixture()
def client() -> TestClient:
    client = TestClient(app)
    client.headers.update({"Authorization": "Bearer OxPqg3cE2P"})
    return client


@pytest.fixture()
def user_email() -> str:
    user_email = 'user_main@gmail.com'
    return user_email


@pytest.fixture()
def user_password() -> str:
    user_password = 'user_main'
    return user_password


@pytest.fixture()
def cfa_image_id() -> int:
    cfa_image_id = 16
    return cfa_image_id


@pytest.fixture()
def cfa_token() -> str:
    cfa_token = "0dWqJonOznuxQUgWVQVDzcddWEQQS3MrBoUkddUulR8PzseOYzh9YJ381RaG1JV0"
    return cfa_token


@pytest.fixture()
def db() -> Session:
    return next(get_db())


@pytest.fixture()
def user_id() -> int:
    return 12


@pytest.fixture()
def seller_bearer_token() -> str:
    return "Xr8F5x6ZvG"
