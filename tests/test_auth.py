from tests.conftest import register_and_login, unique


def test_register_success(client):
    s = unique()
    resp = client.post("/auth/register", json={
        "username": f"user_{s}",
        "email": f"test_{s}@example.com",
        "password": "TestPass123!",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == f"user_{s}"
    assert data["email"] == f"test_{s}@example.com"
    assert "id" in data
    assert "created_at" in data


def test_register_duplicate_email(client):
    s = unique()
    payload = {"username": f"user_{s}", "email": f"dup_{s}@example.com", "password": "Pass123!"}
    client.post("/auth/register", json=payload)
    payload2 = {**payload, "username": f"other_{s}"}
    resp = client.post("/auth/register", json=payload2)
    assert resp.status_code == 400
    assert "Email already registered" in resp.json()["detail"]


def test_register_duplicate_username(client):
    s = unique()
    payload = {"username": f"dupuser_{s}", "email": f"a_{s}@example.com", "password": "Pass123!"}
    client.post("/auth/register", json=payload)
    payload2 = {**payload, "email": f"b_{s}@example.com"}
    resp = client.post("/auth/register", json=payload2)
    assert resp.status_code == 400
    assert "Username already taken" in resp.json()["detail"]


def test_login_success(client):
    creds = register_and_login(client)
    assert creds["token"] is not None


def test_login_wrong_password(client):
    s = unique()
    client.post("/auth/register", json={
        "username": f"u_{s}", "email": f"e_{s}@example.com", "password": "Correct123!"
    })
    resp = client.post("/auth/login", json={"email": f"e_{s}@example.com", "password": "Wrong!"})
    assert resp.status_code == 401


def test_login_nonexistent_user(client):
    resp = client.post("/auth/login", json={"email": "nobody@nowhere.com", "password": "x"})
    assert resp.status_code == 401


def test_protected_route_no_token(client):
    resp = client.get("/users/me")
    assert resp.status_code in (401, 403)
