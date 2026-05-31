"""Document API tests — Phase 6."""

import pytest

USER_PAYLOAD = {
    "email": "document-analyst@example.com",
    "password": "securepass1",
    "full_name": "Document Analyst",
    "role": "analyst",
}

CUSTOMER_PAYLOAD = {
    "external_reference": "CUST-DOC-01",
    "legal_name": "Document Test Corp",
    "customer_type": "business",
}

ALERT_PAYLOAD = {
    "external_reference": "ALERT-DOC-01",
    "alert_type": "manual_review",
    "severity": "medium",
    "title": "Review required",
    "triggered_at": "2026-05-30T09:00:00Z",
}

CASE_PAYLOAD = {
    "external_reference": "CASE-60001",
    "priority": "high",
    "status": "open",
    "title": "Investigation: unusual activity",
    "summary": "Opened from alert triage",
    "opened_at": "2026-05-30T09:30:00Z",
}

DOCUMENT_PAYLOAD = {
    "external_reference": "DOC-60001",
    "document_type": "evidence",
    "file_name": "transaction_report.pdf",
    "file_size": 52341,
    "file_hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
}


async def _seed_customer_alert_case(client) -> tuple[str, str, str]:
    customer = await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    customer_id = customer.json()["id"]
    alert = await client.post(
        "/api/v1/alerts",
        json={**ALERT_PAYLOAD, "customer_id": customer_id},
    )
    alert_id = alert.json()["id"]
    case = await client.post(
        "/api/v1/cases",
        json={**CASE_PAYLOAD, "customer_id": customer_id, "alert_id": alert_id},
    )
    case_id = case.json()["id"]
    return customer_id, alert_id, case_id


@pytest.mark.asyncio
async def test_create_document(client):
    _, _, case_id = await _seed_customer_alert_case(client)
    payload = {**DOCUMENT_PAYLOAD, "case_id": case_id}
    response = await client.post("/api/v1/documents", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["external_reference"] == DOCUMENT_PAYLOAD["external_reference"]
    assert body["case_id"] == case_id
    assert body["document_type"] == "evidence"
    assert body["file_name"] == DOCUMENT_PAYLOAD["file_name"]


@pytest.mark.asyncio
async def test_create_document_unknown_case(client):
    payload = {
        **DOCUMENT_PAYLOAD,
        "case_id": "00000000-0000-0000-0000-000000000099",
    }
    response = await client.post("/api/v1/documents", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_document_with_uploader(client):
    user = await client.post("/api/v1/users", json=USER_PAYLOAD)
    user_id = user.json()["id"]
    _, _, case_id = await _seed_customer_alert_case(client)
    payload = {
        **DOCUMENT_PAYLOAD,
        "case_id": case_id,
        "uploaded_by": user_id,
    }
    response = await client.post("/api/v1/documents", json=payload)
    assert response.status_code == 201
    assert response.json()["uploaded_by"] == user_id


@pytest.mark.asyncio
async def test_create_document_duplicate_reference(client):
    _, _, case_id = await _seed_customer_alert_case(client)
    payload = {**DOCUMENT_PAYLOAD, "case_id": case_id}
    await client.post("/api/v1/documents", json=payload)
    response = await client.post("/api/v1/documents", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_list_documents_by_case(client):
    _, _, case_id = await _seed_customer_alert_case(client)
    await client.post(
        "/api/v1/documents",
        json={**DOCUMENT_PAYLOAD, "case_id": case_id},
    )
    await client.post(
        "/api/v1/documents",
        json={
            **DOCUMENT_PAYLOAD,
            "external_reference": "DOC-60002",
            "case_id": case_id,
            "document_type": "report",
        },
    )
    response = await client.get("/api/v1/documents", params={"case_id": case_id})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2


@pytest.mark.asyncio
async def test_update_document(client):
    _, _, case_id = await _seed_customer_alert_case(client)
    create = await client.post(
        "/api/v1/documents",
        json={**DOCUMENT_PAYLOAD, "case_id": case_id},
    )
    document_id = create.json()["id"]
    response = await client.patch(
        f"/api/v1/documents/{document_id}",
        json={
            "document_type": "statement",
            "file_name": "witness_statement.pdf",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["document_type"] == "statement"
    assert body["file_name"] == "witness_statement.pdf"


@pytest.mark.asyncio
async def test_delete_document(client):
    _, _, case_id = await _seed_customer_alert_case(client)
    create = await client.post(
        "/api/v1/documents",
        json={**DOCUMENT_PAYLOAD, "case_id": case_id},
    )
    document_id = create.json()["id"]
    delete = await client.delete(f"/api/v1/documents/{document_id}")
    assert delete.status_code == 204
    get = await client.get(f"/api/v1/documents/{document_id}")
    assert get.status_code == 404
