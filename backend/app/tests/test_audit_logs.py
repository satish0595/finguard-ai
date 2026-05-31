"""AuditLog API tests — Phase 7."""

import pytest
import uuid as uuid_module

AUDIT_LOG_PAYLOAD = {
    "entity_type": "user",
    "entity_id": "00000000-0000-0000-0000-000000000001",
    "action": "create",
    "old_values": None,
    "new_values": {
        "email": "test@example.com",
        "role": "analyst",
    },
}


@pytest.mark.asyncio
async def test_create_audit_log(client):
    response = await client.post("/api/v1/audit-logs", json=AUDIT_LOG_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["entity_type"] == "user"
    assert body["action"] == "create"
    assert body["new_values"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_create_audit_log_with_old_values(client):
    payload = {
        **AUDIT_LOG_PAYLOAD,
        "action": "update",
        "old_values": {"email": "old@example.com"},
        "new_values": {"email": "new@example.com"},
    }
    response = await client.post("/api/v1/audit-logs", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["action"] == "update"
    assert body["old_values"]["email"] == "old@example.com"
    assert body["new_values"]["email"] == "new@example.com"


@pytest.mark.asyncio
async def test_list_audit_logs_by_entity_type(client):
    # Create multiple audit logs
    await client.post("/api/v1/audit-logs", json=AUDIT_LOG_PAYLOAD)
    await client.post(
        "/api/v1/audit-logs",
        json={
            **AUDIT_LOG_PAYLOAD,
            "entity_type": "customer",
            "entity_id": "00000000-0000-0000-0000-000000000002",
        },
    )
    
    # List only user entity logs
    response = await client.get(
        "/api/v1/audit-logs",
        params={"entity_type": "user"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["entity_type"] == "user"


@pytest.mark.asyncio
async def test_list_audit_logs_by_entity_id(client):
    entity_id = "00000000-0000-0000-0000-000000000001"
    await client.post(
        "/api/v1/audit-logs",
        json={**AUDIT_LOG_PAYLOAD, "entity_id": entity_id},
    )
    await client.post(
        "/api/v1/audit-logs",
        json={
            **AUDIT_LOG_PAYLOAD,
            "entity_id": "00000000-0000-0000-0000-000000000099",
        },
    )
    
    response = await client.get(
        "/api/v1/audit-logs",
        params={"entity_id": entity_id},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["entity_id"] == entity_id


@pytest.mark.asyncio
async def test_list_audit_logs_by_action(client):
    await client.post(
        "/api/v1/audit-logs",
        json={**AUDIT_LOG_PAYLOAD, "action": "create"},
    )
    await client.post(
        "/api/v1/audit-logs",
        json={
            **AUDIT_LOG_PAYLOAD,
            "entity_id": "00000000-0000-0000-0000-000000000002",
            "action": "delete",
        },
    )
    
    response = await client.get(
        "/api/v1/audit-logs",
        params={"action": "delete"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["action"] == "delete"


@pytest.mark.asyncio
async def test_list_audit_logs_pagination(client):
    # Create 5 audit logs
    for i in range(5):
        await client.post(
            "/api/v1/audit-logs",
            json={
                **AUDIT_LOG_PAYLOAD,
                "entity_id": f"00000000-0000-0000-0000-00000000000{i}",
            },
        )
    
    # Test pagination
    response = await client.get(
        "/api/v1/audit-logs",
        params={"skip": 0, "limit": 2},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2


@pytest.mark.asyncio
async def test_list_audit_logs_empty(client):
    response = await client.get("/api/v1/audit-logs")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert len(body["items"]) == 0
