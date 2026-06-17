"""Dashboard API tests."""

import pytest


CUSTOMER_HIGH_RISK = {
    "external_reference": "CUST-DASH-01",
    "legal_name": "Dashboard High Risk Ltd",
    "customer_type": "business",
    "risk_level": "high",
    "status": "pending_review",
}

CUSTOMER_LOW_RISK = {
    "external_reference": "CUST-DASH-02",
    "legal_name": "Dashboard Stable Ltd",
    "customer_type": "business",
    "risk_level": "low",
    "status": "active",
}

TRANSACTION_PAYLOAD = {
    "external_reference": "TXN-DASH-01",
    "amount": "1000.00",
    "currency": "usd",
    "transaction_type": "wire",
    "direction": "outbound",
    "status": "pending",
    "transaction_at": "2026-05-30T14:30:00Z",
}

ALERT_PAYLOAD = {
    "external_reference": "ALERT-DASH-01",
    "alert_type": "unusual_activity",
    "severity": "critical",
    "status": "open",
    "title": "Dashboard alert",
    "triggered_at": "2026-05-30T14:35:00Z",
}

CASE_PAYLOAD = {
    "external_reference": "CASE-DASH-01",
    "priority": "urgent",
    "status": "open",
    "title": "Dashboard case",
    "opened_at": "2026-05-30T14:40:00Z",
}


@pytest.mark.asyncio
async def test_dashboard_summary(client):
    high = await client.post("/api/v1/customers", json=CUSTOMER_HIGH_RISK)
    low = await client.post("/api/v1/customers", json=CUSTOMER_LOW_RISK)
    high_id = high.json()["id"]
    low_id = low.json()["id"]

    await client.post(
        "/api/v1/transactions",
        json={**TRANSACTION_PAYLOAD, "customer_id": high_id},
    )
    await client.post(
        "/api/v1/transactions",
        json={
            **TRANSACTION_PAYLOAD,
            "external_reference": "TXN-DASH-02",
            "customer_id": low_id,
            "status": "completed",
        },
    )
    await client.post(
        "/api/v1/alerts",
        json={**ALERT_PAYLOAD, "customer_id": high_id},
    )
    await client.post(
        "/api/v1/cases",
        json={**CASE_PAYLOAD, "customer_id": high_id},
    )

    response = await client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["customers_total"] == 2
    assert body["customers_high_risk"] == 1
    assert body["customers_pending_review"] == 1
    assert body["transactions_total"] == 2
    assert body["transactions_pending"] == 1
    assert body["open_alerts"] == 1
    assert body["critical_alerts"] == 1
    assert body["open_cases"] == 1
    assert body["urgent_cases"] == 1