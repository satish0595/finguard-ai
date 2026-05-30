"""Customer API tests — Phase 2."""

import pytest

CUSTOMER_PAYLOAD = {
    "external_reference": "CUST-10001",
    "legal_name": "Acme Holdings Ltd",
    "email": "contact@acme.example.com",
    "phone": "+441234567890",
    "customer_type": "business",
    "risk_level": "medium",
    "status": "active",
    "country_code": "GB",
}


@pytest.mark.asyncio
async def test_create_customer(client):
    response = await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["external_reference"] == CUSTOMER_PAYLOAD["external_reference"]
    assert body["legal_name"] == CUSTOMER_PAYLOAD["legal_name"]
    assert body["customer_type"] == "business"
    assert body["risk_level"] == "medium"
    assert "id" in body


@pytest.mark.asyncio
async def test_create_customer_duplicate_reference(client):
    await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    response = await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_customer(client):
    create = await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    customer_id = create.json()["id"]
    response = await client.get(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["legal_name"] == CUSTOMER_PAYLOAD["legal_name"]


@pytest.mark.asyncio
async def test_get_customer_not_found(client):
    response = await client.get(
        "/api/v1/customers/00000000-0000-0000-0000-000000000099"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_customers(client):
    await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    await client.post(
        "/api/v1/customers",
        json={**CUSTOMER_PAYLOAD, "external_reference": "CUST-10002"},
    )
    response = await client.get("/api/v1/customers")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2


@pytest.mark.asyncio
async def test_update_customer(client):
    create = await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    customer_id = create.json()["id"]
    response = await client.patch(
        f"/api/v1/customers/{customer_id}",
        json={"risk_level": "high", "status": "pending_review"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "high"
    assert body["status"] == "pending_review"


@pytest.mark.asyncio
async def test_delete_customer(client):
    create = await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    customer_id = create.json()["id"]
    delete = await client.delete(f"/api/v1/customers/{customer_id}")
    assert delete.status_code == 204
    get = await client.get(f"/api/v1/customers/{customer_id}")
    assert get.status_code == 404
