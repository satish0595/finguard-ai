"""PolicyChunk API tests — Phase 8."""

import pytest

POLICY_CHUNK_PAYLOAD = {
    "external_reference": "POL-CHK-80001",
    "policy_name": "KYC Policy",
    "chunk_index": 0,
    "content": "Know Your Customer (KYC) policy outlines requirements for customer identification and verification...",
    "tags": ["kyc", "verification", "required"],
}


@pytest.mark.asyncio
async def test_create_policy_chunk(client):
    response = await client.post("/api/v1/policy-chunks", json=POLICY_CHUNK_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["external_reference"] == POLICY_CHUNK_PAYLOAD["external_reference"]
    assert body["policy_name"] == POLICY_CHUNK_PAYLOAD["policy_name"]
    assert body["chunk_index"] == 0
    assert body["tags"] == ["kyc", "verification", "required"]


@pytest.mark.asyncio
async def test_create_policy_chunk_duplicate_reference(client):
    payload = {**POLICY_CHUNK_PAYLOAD}
    await client.post("/api/v1/policy-chunks", json=payload)
    response = await client.post("/api/v1/policy-chunks", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_policy_chunk_minimal(client):
    payload = {
        "external_reference": "POL-CHK-80002",
        "policy_name": "AML Policy",
        "chunk_index": 1,
        "content": "Anti-Money Laundering policy defines procedures...",
    }
    response = await client.post("/api/v1/policy-chunks", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["tags"] is None


@pytest.mark.asyncio
async def test_get_policy_chunk(client):
    create = await client.post("/api/v1/policy-chunks", json=POLICY_CHUNK_PAYLOAD)
    chunk_id = create.json()["id"]
    response = await client.get(f"/api/v1/policy-chunks/{chunk_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == chunk_id
    assert body["external_reference"] == POLICY_CHUNK_PAYLOAD["external_reference"]


@pytest.mark.asyncio
async def test_get_policy_chunk_not_found(client):
    response = await client.get(
        "/api/v1/policy-chunks/00000000-0000-0000-0000-000000000099"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_policy_chunks_by_policy_name(client):
    await client.post("/api/v1/policy-chunks", json=POLICY_CHUNK_PAYLOAD)
    await client.post(
        "/api/v1/policy-chunks",
        json={
            **POLICY_CHUNK_PAYLOAD,
            "external_reference": "POL-CHK-80003",
            "policy_name": "AML Policy",
        },
    )

    response = await client.get(
        "/api/v1/policy-chunks",
        params={"policy_name": "KYC Policy"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["policy_name"] == "KYC Policy"


@pytest.mark.asyncio
async def test_list_policy_chunks_pagination(client):
    # Create 5 policy chunks with same policy name
    for i in range(5):
        await client.post(
            "/api/v1/policy-chunks",
            json={
                **POLICY_CHUNK_PAYLOAD,
                "external_reference": f"POL-CHK-8000{i}",
                "chunk_index": i,
            },
        )

    response = await client.get(
        "/api/v1/policy-chunks",
        params={"skip": 0, "limit": 2},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2


@pytest.mark.asyncio
async def test_update_policy_chunk(client):
    create = await client.post("/api/v1/policy-chunks", json=POLICY_CHUNK_PAYLOAD)
    chunk_id = create.json()["id"]
    response = await client.patch(
        f"/api/v1/policy-chunks/{chunk_id}",
        json={
            "content": "Updated policy content...",
            "tags": ["kyc", "updated"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["content"] == "Updated policy content..."
    assert body["tags"] == ["kyc", "updated"]


@pytest.mark.asyncio
async def test_delete_policy_chunk(client):
    create = await client.post("/api/v1/policy-chunks", json=POLICY_CHUNK_PAYLOAD)
    chunk_id = create.json()["id"]
    delete = await client.delete(f"/api/v1/policy-chunks/{chunk_id}")
    assert delete.status_code == 204
    get = await client.get(f"/api/v1/policy-chunks/{chunk_id}")
    assert get.status_code == 404
