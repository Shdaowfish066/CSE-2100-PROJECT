import uuid
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


def unique() -> str:
    return uuid.uuid4().hex[:10]


def register_and_login(client: TestClient, suffix: str = None) -> dict:
    s = suffix or unique()
    email = f"test_{s}@example.com"
    username = f"user_{s}"
    password = "TestPass123!"

    client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password,
    })

    resp = client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    token = resp.json()["access_token"]

    return {
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"},
        "email": email,
        "username": username,
        "password": password,
    }
