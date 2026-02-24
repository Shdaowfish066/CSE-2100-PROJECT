from tests.conftest import register_and_login, unique


def test_get_me(client):
    user = register_and_login(client)
    resp = client.get("/users/me", headers=user["headers"])
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == user["username"]
    assert data["email"] == user["email"]
    assert "created_at" in data


def test_get_me_no_auth(client):
    resp = client.get("/users/me")
    assert resp.status_code in (401, 403)


def test_get_user_by_id(client):
    user = register_and_login(client)
    me = client.get("/users/me", headers=user["headers"]).json()
    resp = client.get(f"/users/{me['id']}")
    assert resp.status_code == 200
    assert resp.json()["username"] == user["username"]


def test_get_nonexistent_user(client):
    resp = client.get("/users/9999999")
    assert resp.status_code == 404


def test_get_user_by_username(client):
    user = register_and_login(client)
    resp = client.get(f"/users/by-username/{user['username']}")
    assert resp.status_code == 200
    assert resp.json()["email"] == user["email"]


def test_update_username(client):
    user = register_and_login(client)
    me = client.get("/users/me", headers=user["headers"]).json()
    new_name = f"newname_{unique()}"
    resp = client.put(f"/users/{me['id']}", json={"username": new_name}, headers=user["headers"])
    assert resp.status_code == 200


def test_update_another_user_forbidden(client):
    user_a = register_and_login(client)
    user_b = register_and_login(client)
    me_b = client.get("/users/me", headers=user_b["headers"]).json()
    resp = client.put(f"/users/{me_b['id']}", json={"username": f"x_{unique()}"}, headers=user_a["headers"])
    assert resp.status_code == 403
