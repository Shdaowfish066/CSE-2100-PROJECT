from tests.conftest import register_and_login, unique


def _create_community(client, headers, name=None):
    return client.post("/communities/", json={
        "name": name or f"comm_{unique()}",
        "description": "A test community",
    }, headers=headers)


def test_create_community(client):
    user = register_and_login(client)
    resp = _create_community(client, user["headers"])
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert "id" in data
    assert "created_at" in data
    assert data["captain_id"] is not None


def test_create_community_unauthenticated(client):
    resp = client.post("/communities/", json={"name": f"c_{unique()}"})
    assert resp.status_code in (401, 403)


def test_list_communities(client):
    user = register_and_login(client)
    _create_community(client, user["headers"])
    resp = client.get("/communities/", headers=user["headers"])
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_list_communities_unauthenticated(client):
    resp = client.get("/communities/")
    assert resp.status_code in (401, 403)


def test_get_community(client):
    user = register_and_login(client)
    comm_id = _create_community(client, user["headers"]).json()["data"]["id"]
    resp = client.get(f"/communities/{comm_id}", headers=user["headers"])
    assert resp.status_code == 200
    assert resp.json()["id"] == comm_id


def test_get_nonexistent_community(client):
    user = register_and_login(client)
    resp = client.get("/communities/9999999", headers=user["headers"])
    assert resp.status_code == 404


def test_join_community(client):
    captain = register_and_login(client)
    member = register_and_login(client)
    comm_id = _create_community(client, captain["headers"]).json()["data"]["id"]
    resp = client.post(f"/communities/{comm_id}/join", headers=member["headers"])
    assert resp.status_code == 200


def test_join_already_member(client):
    captain = register_and_login(client)
    comm_id = _create_community(client, captain["headers"]).json()["data"]["id"]
    resp = client.post(f"/communities/{comm_id}/join", headers=captain["headers"])
    assert resp.status_code == 400


def test_create_community_post(client):
    captain = register_and_login(client)
    comm_id = _create_community(client, captain["headers"]).json()["data"]["id"]
    resp = client.post(f"/communities/{comm_id}/posts/", json={
        "title": "Community post", "content": "Some content"
    }, headers=captain["headers"])
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert "created_at" in data


def test_community_post_requires_membership(client):
    captain = register_and_login(client)
    outsider = register_and_login(client)
    comm_id = _create_community(client, captain["headers"]).json()["data"]["id"]
    resp = client.post(f"/communities/{comm_id}/posts/", json={
        "title": "Sneak in", "content": "No permission"
    }, headers=outsider["headers"])
    assert resp.status_code == 403


def test_list_community_posts(client):
    captain = register_and_login(client)
    comm_id = _create_community(client, captain["headers"]).json()["data"]["id"]
    client.post(f"/communities/{comm_id}/posts/", json={
        "title": "P1", "content": "C1"
    }, headers=captain["headers"])
    resp = client.get(f"/communities/{comm_id}/posts/", headers=captain["headers"])
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_list_community_members(client):
    captain = register_and_login(client)
    member = register_and_login(client)
    comm_id = _create_community(client, captain["headers"]).json()["data"]["id"]
    client.post(f"/communities/{comm_id}/join", headers=member["headers"])
    resp = client.get(f"/communities/{comm_id}/members", headers=captain["headers"])
    assert resp.status_code == 200
    members = resp.json()
    assert len(members) >= 2
    assert any("joined_at" in m for m in members)


def test_leave_community(client):
    captain = register_and_login(client)
    member = register_and_login(client)
    comm_id = _create_community(client, captain["headers"]).json()["data"]["id"]
    client.post(f"/communities/{comm_id}/join", headers=member["headers"])
    resp = client.post(f"/communities/{comm_id}/leave", headers=member["headers"])
    assert resp.status_code == 200


def test_duplicate_community_name(client):
    captain = register_and_login(client)
    name = f"unique_{unique()}"
    _create_community(client, captain["headers"], name=name)
    resp = _create_community(client, captain["headers"], name=name)
    assert resp.status_code == 400
