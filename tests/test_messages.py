from tests.conftest import register_and_login, unique


def test_send_message(client):
    sender = register_and_login(client)
    receiver = register_and_login(client)
    receiver_id = client.get("/users/me", headers=receiver["headers"]).json()["id"]

    resp = client.post("/messages/", json={
        "recipient_id": receiver_id,
        "content": "Hello there!",
    }, headers=sender["headers"])
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["content"] == "Hello there!"
    assert data["sender_id"] is not None


def test_send_message_to_nonexistent_user(client):
    sender = register_and_login(client)
    resp = client.post("/messages/", json={
        "recipient_id": 9999999,
        "content": "Ghost message",
    }, headers=sender["headers"])
    assert resp.status_code == 404


def test_get_inbox(client):
    sender = register_and_login(client)
    receiver = register_and_login(client)
    receiver_id = client.get("/users/me", headers=receiver["headers"]).json()["id"]

    client.post("/messages/", json={"recipient_id": receiver_id, "content": "Msg 1"}, headers=sender["headers"])
    client.post("/messages/", json={"recipient_id": receiver_id, "content": "Msg 2"}, headers=sender["headers"])

    resp = client.get("/messages/inbox", headers=receiver["headers"])
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_get_conversation(client):
    user_a = register_and_login(client)
    user_b = register_and_login(client)
    id_b = client.get("/users/me", headers=user_b["headers"]).json()["id"]
    id_a = client.get("/users/me", headers=user_a["headers"]).json()["id"]

    client.post("/messages/", json={"recipient_id": id_b, "content": "Hey B"}, headers=user_a["headers"])
    client.post("/messages/", json={"recipient_id": id_a, "content": "Hey A"}, headers=user_b["headers"])

    resp = client.get(f"/messages/conversation/{id_b}", headers=user_a["headers"])
    assert resp.status_code == 200
    messages = resp.json()
    assert len(messages) >= 2
    contents = [m["content"] for m in messages]
    assert "Hey B" in contents
    assert "Hey A" in contents


def test_message_requires_auth(client):
    resp = client.post("/messages/", json={"recipient_id": 1, "content": "No auth"})
    assert resp.status_code in (401, 403)
