"""User API tests — Phase 1."""

import pytest

USER_PAYLOAD = {
    "email": "analyst@example.com",
    "password": "securepass1",
    "full_name": "Test Analyst",
    "role": "analyst",
}


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/api/v1/users", json=USER_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == USER_PAYLOAD["email"]
    assert body["full_name"] == USER_PAYLOAD["full_name"]
    assert body["role"] == "analyst"
    assert body["is_active"] is True
    assert "id" in body
    assert "hashed_password" not in body
    assert "password" not in body


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client):
    await client.post("/api/v1/users", json=USER_PAYLOAD)
    response = await client.post("/api/v1/users", json=USER_PAYLOAD)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_user(client):
    create = await client.post("/api/v1/users", json=USER_PAYLOAD)
    user_id = create.json()["id"]
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == USER_PAYLOAD["email"]


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get(
        "/api/v1/users/00000000-0000-0000-0000-000000000099"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_by_email(client):
    await client.post("/api/v1/users", json=USER_PAYLOAD)
    response = await client.get("/api/v1/users/by-email", params={"email": USER_PAYLOAD["email"]})
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == USER_PAYLOAD["email"]


@pytest.mark.asyncio
async def test_list_users(client):
    await client.post("/api/v1/users", json=USER_PAYLOAD)
    await client.post(
        "/api/v1/users",
        json={**USER_PAYLOAD, "email": "second@example.com"},
    )
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2


@pytest.mark.asyncio
async def test_update_user(client):
    create = await client.post("/api/v1/users", json=USER_PAYLOAD)
    user_id = create.json()["id"]
    response = await client.patch(
        f"/api/v1/users/{user_id}",
        json={"full_name": "Updated Name", "role": "admin"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["full_name"] == "Updated Name"
    assert body["role"] == "admin"


@pytest.mark.asyncio
async def test_delete_user(client):
    create = await client.post("/api/v1/users", json=USER_PAYLOAD)
    user_id = create.json()["id"]
    delete = await client.delete(f"/api/v1/users/{user_id}")
    assert delete.status_code == 204
    get = await client.get(f"/api/v1/users/{user_id}")
    assert get.status_code == 404
