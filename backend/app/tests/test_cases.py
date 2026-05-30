"""Case API tests — Phase 5."""

import pytest

USER_PAYLOAD = {
    "email": "case-analyst@example.com",
    "password": "securepass1",
    "full_name": "Case Analyst",
    "role": "analyst",
}

CUSTOMER_PAYLOAD = {
    "external_reference": "CUST-CASE-01",
    "legal_name": "Case Test Corp",
    "customer_type": "business",
}

ALERT_PAYLOAD = {
    "external_reference": "ALERT-CASE-01",
    "alert_type": "manual_review",
    "severity": "medium",
    "title": "Review required",
    "triggered_at": "2026-05-30T09:00:00Z",
}

CASE_PAYLOAD = {
    "external_reference": "CASE-50001",
    "priority": "high",
    "status": "open",
    "title": "Investigation: unusual activity",
    "summary": "Opened from alert triage",
    "opened_at": "2026-05-30T09:30:00Z",
}


async def _seed_customer_and_alert(client) -> tuple[str, str]:
    customer = await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    customer_id = customer.json()["id"]
    alert = await client.post(
        "/api/v1/alerts",
        json={**ALERT_PAYLOAD, "customer_id": customer_id},
    )
    return customer_id, alert.json()["id"]


@pytest.mark.asyncio
async def test_create_case(client):
    customer_id, alert_id = await _seed_customer_and_alert(client)
    payload = {**CASE_PAYLOAD, "customer_id": customer_id, "alert_id": alert_id}
    response = await client.post("/api/v1/cases", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["external_reference"] == CASE_PAYLOAD["external_reference"]
    assert body["alert_id"] == alert_id
    assert body["priority"] == "high"


@pytest.mark.asyncio
async def test_create_case_unknown_customer(client):
    payload = {
        **CASE_PAYLOAD,
        "customer_id": "00000000-0000-0000-0000-000000000099",
    }
    response = await client.post("/api/v1/cases", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_case_alert_customer_mismatch(client):
    customer_id, _ = await _seed_customer_and_alert(client)
    other = await client.post(
        "/api/v1/customers",
        json={**CUSTOMER_PAYLOAD, "external_reference": "CUST-CASE-02"},
    )
    other_id = other.json()["id"]
    alert = await client.post(
        "/api/v1/alerts",
        json={
            **ALERT_PAYLOAD,
            "customer_id": other_id,
            "external_reference": "ALERT-CASE-02",
        },
    )
    payload = {
        **CASE_PAYLOAD,
        "customer_id": customer_id,
        "alert_id": alert.json()["id"],
    }
    response = await client.post("/api/v1/cases", json=payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_case_with_assignee(client):
    user = await client.post("/api/v1/users", json=USER_PAYLOAD)
    user_id = user.json()["id"]
    customer_id, _ = await _seed_customer_and_alert(client)
    payload = {
        **CASE_PAYLOAD,
        "external_reference": "CASE-50002",
        "customer_id": customer_id,
        "assigned_to": user_id,
    }
    response = await client.post("/api/v1/cases", json=payload)
    assert response.status_code == 201
    assert response.json()["assigned_to"] == user_id


@pytest.mark.asyncio
async def test_list_cases_by_status(client):
    customer_id, _ = await _seed_customer_and_alert(client)
    await client.post(
        "/api/v1/cases",
        json={**CASE_PAYLOAD, "customer_id": customer_id},
    )
    await client.post(
        "/api/v1/cases",
        json={
            **CASE_PAYLOAD,
            "external_reference": "CASE-50003",
            "customer_id": customer_id,
            "status": "closed",
            "closed_at": "2026-05-31T10:00:00Z",
        },
    )
    response = await client.get(
        "/api/v1/cases", params={"status": "open", "customer_id": customer_id}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["status"] == "open"


@pytest.mark.asyncio
async def test_update_case(client):
    customer_id, alert_id = await _seed_customer_and_alert(client)
    create = await client.post(
        "/api/v1/cases",
        json={**CASE_PAYLOAD, "customer_id": customer_id, "alert_id": alert_id},
    )
    case_id = create.json()["id"]
    response = await client.patch(
        f"/api/v1/cases/{case_id}",
        json={
            "status": "in_progress",
            "priority": "urgent",
            "summary": "Escalated after review",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "in_progress"
    assert body["priority"] == "urgent"


@pytest.mark.asyncio
async def test_delete_case(client):
    customer_id, _ = await _seed_customer_and_alert(client)
    create = await client.post(
        "/api/v1/cases",
        json={**CASE_PAYLOAD, "customer_id": customer_id},
    )
    case_id = create.json()["id"]
    delete = await client.delete(f"/api/v1/cases/{case_id}")
    assert delete.status_code == 204
    get = await client.get(f"/api/v1/cases/{case_id}")
    assert get.status_code == 404
