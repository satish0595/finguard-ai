"""Transaction API routes — Phase 3."""

import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_transaction_service
from app.schemas.transaction import (
    TransactionCreate,
    TransactionList,
    TransactionRead,
    TransactionUpdate,
)
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: TransactionCreate,
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.create_transaction(payload)


@router.get("", response_model=TransactionList)
async def list_transactions(
    customer_id: uuid.UUID | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: TransactionService = Depends(get_transaction_service),
):
    items, total = await service.list_transactions(
        customer_id=customer_id, skip=skip, limit=limit
    )
    return TransactionList(items=items, total=total)


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    transaction_id: uuid.UUID,
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.get_transaction(transaction_id)


@router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: uuid.UUID,
    payload: TransactionUpdate,
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.update_transaction(transaction_id, payload)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: uuid.UUID,
    service: TransactionService = Depends(get_transaction_service),
):
    await service.delete_transaction(transaction_id)
