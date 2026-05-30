"""Alert API tests — Phase 4."""

import pytest

USER_PAYLOAD = {
    "email": "alert-analyst@example.com",
    "password": "securepass1",
    "full_name": "Alert Analyst",
    "role": "analyst",
}

CUSTOMER_PAYLOAD = {
    "external_reference": "CUST-ALERT-01",
    "legal_name": "Alert Test Corp",
    "customer_type": "business",
}

TRANSACTION_PAYLOAD = {
    "external_reference": "TXN-ALERT-01",
    "amount": "5000.00",
    "currency": "USD",
    "transaction_type": "wire",
    "direction": "outbound",
    "transaction_at": "2026-05-30T10:00:00Z",
}

ALERT_PAYLOAD = {
    "external_reference": "ALERT-70001",
    "alert_type": "unusual_activity",
    "severity": "high",
    "status": "open",
    "title": "Large outbound wire",
    "description": "Amount exceeds daily threshold",
    "triggered_at": "2026-05-30T10:05:00Z",
}


async def _seed_customer_and_transaction(client) -> tuple[str, str]:
    customer = await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    customer_id = customer.json()["id"]
    txn = await client.post(
        "/api/v1/transactions",
        json={**TRANSACTION_PAYLOAD, "customer_id": customer_id},
    )
    return customer_id, txn.json()["id"]


@pytest.mark.asyncio
async def test_create_alert(client):
    customer_id, transaction_id = await _seed_customer_and_transaction(client)
    payload = {
        **ALERT_PAYLOAD,
        "customer_id": customer_id,
        "transaction_id": transaction_id,
    }
    response = await client.post("/api/v1/alerts", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["external_reference"] == ALERT_PAYLOAD["external_reference"]
    assert body["severity"] == "high"
    assert body["transaction_id"] == transaction_id


@pytest.mark.asyncio
async def test_create_alert_unknown_customer(client):
    payload = {
        **ALERT_PAYLOAD,
        "customer_id": "00000000-0000-0000-0000-000000000099",
    }
    response = await client.post("/api/v1/alerts", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_alert_transaction_customer_mismatch(client):
    customer_id, _ = await _seed_customer_and_transaction(client)
    other = await client.post(
        "/api/v1/customers",
        json={**CUSTOMER_PAYLOAD, "external_reference": "CUST-ALERT-02"},
    )
    other_id = other.json()["id"]
    txn = await client.post(
        "/api/v1/transactions",
        json={
            **TRANSACTION_PAYLOAD,
            "customer_id": other_id,
            "external_reference": "TXN-ALERT-02",
        },
    )
    payload = {
        **ALERT_PAYLOAD,
        "customer_id": customer_id,
        "transaction_id": txn.json()["id"],
    }
    response = await client.post("/api/v1/alerts", json=payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_alert_with_assignee(client):
    user = await client.post("/api/v1/users", json=USER_PAYLOAD)
    user_id = user.json()["id"]
    customer_id, _ = await _seed_customer_and_transaction(client)
    payload = {
        **ALERT_PAYLOAD,
        "external_reference": "ALERT-70002",
        "customer_id": customer_id,
        "assigned_to": user_id,
    }
    response = await client.post("/api/v1/alerts", json=payload)
    assert response.status_code == 201
    assert response.json()["assigned_to"] == user_id


@pytest.mark.asyncio
async def test_list_alerts_by_status(client):
    customer_id, _ = await _seed_customer_and_transaction(client)
    await client.post(
        "/api/v1/alerts",
        json={**ALERT_PAYLOAD, "customer_id": customer_id},
    )
    await client.post(
        "/api/v1/alerts",
        json={
            **ALERT_PAYLOAD,
            "external_reference": "ALERT-70003",
            "customer_id": customer_id,
            "status": "closed",
        },
    )
    response = await client.get(
        "/api/v1/alerts", params={"status": "open", "customer_id": customer_id}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["status"] == "open"


@pytest.mark.asyncio
async def test_update_alert(client):
    customer_id, _ = await _seed_customer_and_transaction(client)
    create = await client.post(
        "/api/v1/alerts",
        json={**ALERT_PAYLOAD, "customer_id": customer_id},
    )
    alert_id = create.json()["id"]
    response = await client.patch(
        f"/api/v1/alerts/{alert_id}",
        json={
            "status": "investigating",
            "severity": "critical",
            "resolved_at": "2026-05-30T12:00:00Z",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "investigating"
    assert body["severity"] == "critical"


@pytest.mark.asyncio
async def test_delete_alert(client):
    customer_id, _ = await _seed_customer_and_transaction(client)
    create = await client.post(
        "/api/v1/alerts",
        json={**ALERT_PAYLOAD, "customer_id": customer_id},
    )
    alert_id = create.json()["id"]
    delete = await client.delete(f"/api/v1/alerts/{alert_id}")
    assert delete.status_code == 204
    get = await client.get(f"/api/v1/alerts/{alert_id}")
    assert get.status_code == 404
