from tests.conftest import register_and_login, unique


def _setup(client):
    user = register_and_login(client)
    post_resp = client.post("/posts/", json={
        "title": f"Post {unique()}", "content": "Content", "is_anonymous": False
    }, headers=user["headers"])
    post_id = post_resp.json()["data"]["id"]
    return user, post_id


def test_create_comment(client):
    user, post_id = _setup(client)
    resp = client.post(f"/comments/{post_id}", json={"content": "Nice post!"}, headers=user["headers"])
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["content"] == "Nice post!"
    assert data["post_id"] == post_id
    assert "created_at" in data


def test_create_comment_on_nonexistent_post(client):
    user = register_and_login(client)
    resp = client.post("/comments/9999999", json={"content": "Hi"}, headers=user["headers"])
    assert resp.status_code == 404


def test_list_comments(client):
    user, post_id = _setup(client)
    client.post(f"/comments/{post_id}", json={"content": "Comment 1"}, headers=user["headers"])
    client.post(f"/comments/{post_id}", json={"content": "Comment 2"}, headers=user["headers"])
    resp = client.get(f"/comments/post/{post_id}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


def test_get_comment_by_id(client):
    user, post_id = _setup(client)
    comment_id = client.post(
        f"/comments/{post_id}", json={"content": "Hello"}, headers=user["headers"]
    ).json()["data"]["id"]
    resp = client.get(f"/comments/{comment_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == comment_id


def test_get_nonexistent_comment(client):
    resp = client.get("/comments/9999999")
    assert resp.status_code == 404


def test_update_comment(client):
    user, post_id = _setup(client)
    comment_id = client.post(
        f"/comments/{post_id}", json={"content": "Old"}, headers=user["headers"]
    ).json()["data"]["id"]
    resp = client.put(f"/comments/{comment_id}", json={"content": "Updated"}, headers=user["headers"])
    assert resp.status_code == 200


def test_update_comment_by_another_user(client):
    owner, post_id = _setup(client)
    other = register_and_login(client)
    comment_id = client.post(
        f"/comments/{post_id}", json={"content": "Mine"}, headers=owner["headers"]
    ).json()["data"]["id"]
    resp = client.put(f"/comments/{comment_id}", json={"content": "Stolen"}, headers=other["headers"])
    assert resp.status_code == 403


def test_delete_comment(client):
    user, post_id = _setup(client)
    comment_id = client.post(
        f"/comments/{post_id}", json={"content": "Delete me"}, headers=user["headers"]
    ).json()["data"]["id"]
    resp = client.delete(f"/comments/{comment_id}", headers=user["headers"])
    assert resp.status_code == 200
    assert client.get(f"/comments/{comment_id}").status_code == 404
