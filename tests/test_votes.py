from tests.conftest import register_and_login, unique


def _make_post(client, headers):
    resp = client.post("/posts/", json={
        "title": f"Post {unique()}", "content": "Content", "is_anonymous": False
    }, headers=headers)
    return resp.json()["data"]["id"]


def _make_comment(client, headers, post_id):
    resp = client.post(f"/comments/{post_id}", json={"content": "Comment"}, headers=headers)
    return resp.json()["data"]["id"]


def test_upvote_post(client):
    user = register_and_login(client)
    post_id = _make_post(client, user["headers"])
    resp = client.post(f"/votes/post/{post_id}", json={"vote_type": "upvote"}, headers=user["headers"])
    assert resp.status_code == 201
    assert resp.json()["data"]["vote_type"] == "upvote"
    assert "created_at" in resp.json()["data"]


def test_downvote_post(client):
    user = register_and_login(client)
    post_id = _make_post(client, user["headers"])
    resp = client.post(f"/votes/post/{post_id}", json={"vote_type": "downvote"}, headers=user["headers"])
    assert resp.status_code == 201


def test_change_vote_on_post(client):
    user = register_and_login(client)
    post_id = _make_post(client, user["headers"])
    client.post(f"/votes/post/{post_id}", json={"vote_type": "upvote"}, headers=user["headers"])
    resp = client.post(f"/votes/post/{post_id}", json={"vote_type": "downvote"}, headers=user["headers"])
    assert resp.status_code == 201
    assert resp.json()["data"]["vote_type"] == "downvote"


def test_vote_nonexistent_post(client):
    user = register_and_login(client)
    resp = client.post("/votes/post/9999999", json={"vote_type": "upvote"}, headers=user["headers"])
    assert resp.status_code == 404


def test_unvote_post(client):
    user = register_and_login(client)
    post_id = _make_post(client, user["headers"])
    client.post(f"/votes/post/{post_id}", json={"vote_type": "upvote"}, headers=user["headers"])
    resp = client.delete(f"/votes/post/{post_id}", headers=user["headers"])
    assert resp.status_code == 200


def test_get_post_vote_score(client):
    user = register_and_login(client)
    post_id = _make_post(client, user["headers"])
    client.post(f"/votes/post/{post_id}", json={"vote_type": "upvote"}, headers=user["headers"])
    resp = client.get(f"/votes/post/{post_id}/score")
    assert resp.status_code == 200
    body = resp.json()
    assert "upvotes" in body
    assert "downvotes" in body
    assert body["upvotes"] >= 1


def test_upvote_comment(client):
    user = register_and_login(client)
    post_id = _make_post(client, user["headers"])
    comment_id = _make_comment(client, user["headers"], post_id)
    resp = client.post(f"/votes/comment/{comment_id}", json={"vote_type": "upvote"}, headers=user["headers"])
    assert resp.status_code == 201


def test_unvote_comment(client):
    user = register_and_login(client)
    post_id = _make_post(client, user["headers"])
    comment_id = _make_comment(client, user["headers"], post_id)
    client.post(f"/votes/comment/{comment_id}", json={"vote_type": "upvote"}, headers=user["headers"])
    resp = client.delete(f"/votes/comment/{comment_id}", headers=user["headers"])
    assert resp.status_code == 200
