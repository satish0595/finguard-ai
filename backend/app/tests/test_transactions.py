"""Transaction API tests — Phase 3."""

import pytest

CUSTOMER_PAYLOAD = {
    "external_reference": "CUST-TXN-01",
    "legal_name": "Txn Test Corp",
    "customer_type": "business",
}

TRANSACTION_PAYLOAD = {
    "external_reference": "TXN-90001",
    "amount": "1500.50",
    "currency": "usd",
    "transaction_type": "wire",
    "direction": "outbound",
    "status": "pending",
    "counterparty_name": "Supplier Ltd",
    "transaction_at": "2026-05-30T14:30:00Z",
}


async def _create_customer(client) -> str:
    response = await client.post("/api/v1/customers", json=CUSTOMER_PAYLOAD)
    assert response.status_code == 201
    return response.json()["id"]


@pytest.mark.asyncio
async def test_create_transaction(client):
    customer_id = await _create_customer(client)
    payload = {**TRANSACTION_PAYLOAD, "customer_id": customer_id}
    response = await client.post("/api/v1/transactions", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["external_reference"] == TRANSACTION_PAYLOAD["external_reference"]
    assert body["amount"] == "1500.50"
    assert body["currency"] == "USD"
    assert body["customer_id"] == customer_id


@pytest.mark.asyncio
async def test_create_transaction_unknown_customer(client):
    payload = {
        **TRANSACTION_PAYLOAD,
        "customer_id": "00000000-0000-0000-0000-000000000099",
    }
    response = await client.post("/api/v1/transactions", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_transaction_duplicate_reference(client):
    customer_id = await _create_customer(client)
    payload = {**TRANSACTION_PAYLOAD, "customer_id": customer_id}
    await client.post("/api/v1/transactions", json=payload)
    response = await client.post("/api/v1/transactions", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_transaction(client):
    customer_id = await _create_customer(client)
    create = await client.post(
        "/api/v1/transactions",
        json={**TRANSACTION_PAYLOAD, "customer_id": customer_id},
    )
    txn_id = create.json()["id"]
    response = await client.get(f"/api/v1/transactions/{txn_id}")
    assert response.status_code == 200
    assert response.json()["external_reference"] == TRANSACTION_PAYLOAD["external_reference"]


@pytest.mark.asyncio
async def test_list_transactions_by_customer(client):
    customer_id = await _create_customer(client)
    other = await client.post(
        "/api/v1/customers",
        json={**CUSTOMER_PAYLOAD, "external_reference": "CUST-TXN-02"},
    )
    other_id = other.json()["id"]
    await client.post(
        "/api/v1/transactions",
        json={
            **TRANSACTION_PAYLOAD,
            "customer_id": customer_id,
            "external_reference": "TXN-90001",
        },
    )
    await client.post(
        "/api/v1/transactions",
        json={
            **TRANSACTION_PAYLOAD,
            "customer_id": other_id,
            "external_reference": "TXN-90002",
        },
    )
    response = await client.get(
        "/api/v1/transactions", params={"customer_id": customer_id}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["customer_id"] == customer_id


@pytest.mark.asyncio
async def test_update_transaction(client):
    customer_id = await _create_customer(client)
    create = await client.post(
        "/api/v1/transactions",
        json={**TRANSACTION_PAYLOAD, "customer_id": customer_id},
    )
    txn_id = create.json()["id"]
    response = await client.patch(
        f"/api/v1/transactions/{txn_id}",
        json={"status": "completed", "amount": "2000.00"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["amount"] == "2000.00"


@pytest.mark.asyncio
async def test_delete_transaction(client):
    customer_id = await _create_customer(client)
    create = await client.post(
        "/api/v1/transactions",
        json={**TRANSACTION_PAYLOAD, "customer_id": customer_id},
    )
    txn_id = create.json()["id"]
    delete = await client.delete(f"/api/v1/transactions/{txn_id}")
    assert delete.status_code == 204
    get = await client.get(f"/api/v1/transactions/{txn_id}")
    assert get.status_code == 404
