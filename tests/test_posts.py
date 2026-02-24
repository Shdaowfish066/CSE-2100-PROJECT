from tests.conftest import register_and_login, unique


def _create_post(client, headers, title=None, content=None, anonymous=False):
    return client.post("/posts/", json={
        "title": title or f"Post {unique()}",
        "content": content or "Some content here.",
        "is_anonymous": anonymous,
    }, headers=headers)


def test_create_post_authenticated(client):
    user = register_and_login(client)
    resp = _create_post(client, user["headers"])
    assert resp.status_code == 201
    assert resp.json()["message"] == "Successfully created post"
    data = resp.json()["data"]
    assert "id" in data
    assert "created_at" in data


def test_create_post_unauthenticated(client):
    resp = client.post("/posts/", json={"title": "T", "content": "C"})
    assert resp.status_code in (401, 403)


def test_create_anonymous_post(client):
    user = register_and_login(client)
    resp = _create_post(client, user["headers"], anonymous=True)
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["display_name"] != user["username"]


def test_list_posts(client):
    resp = client.get("/posts/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_post_by_id(client):
    user = register_and_login(client)
    created = _create_post(client, user["headers"]).json()["data"]
    resp = client.get(f"/posts/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_nonexistent_post(client):
    resp = client.get("/posts/9999999")
    assert resp.status_code == 404


def test_get_my_posts(client):
    user = register_and_login(client)
    _create_post(client, user["headers"])
    resp = client.get("/posts/me", headers=user["headers"])
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_update_post(client):
    user = register_and_login(client)
    post_id = _create_post(client, user["headers"]).json()["data"]["id"]
    resp = client.put(f"/posts/{post_id}", json={"title": "Updated Title"}, headers=user["headers"])
    assert resp.status_code == 200


def test_update_post_by_another_user(client):
    owner = register_and_login(client)
    other = register_and_login(client)
    post_id = _create_post(client, owner["headers"]).json()["data"]["id"]
    resp = client.put(f"/posts/{post_id}", json={"title": "Stolen"}, headers=other["headers"])
    assert resp.status_code == 403


def test_delete_post(client):
    user = register_and_login(client)
    post_id = _create_post(client, user["headers"]).json()["data"]["id"]
    resp = client.delete(f"/posts/{post_id}", headers=user["headers"])
    assert resp.status_code == 200
    assert client.get(f"/posts/{post_id}").status_code == 404


def test_delete_post_by_another_user(client):
    owner = register_and_login(client)
    other = register_and_login(client)
    post_id = _create_post(client, owner["headers"]).json()["data"]["id"]
    resp = client.delete(f"/posts/{post_id}", headers=other["headers"])
    assert resp.status_code == 403
