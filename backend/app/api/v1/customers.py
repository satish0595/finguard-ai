"""Customer API routes — Phase 2."""

import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_customer_service
from app.schemas.customer import (
    CustomerCreate,
    CustomerList,
    CustomerRead,
    CustomerUpdate,
)
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
async def create_customer(
    payload: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.create_customer(payload)


@router.get("", response_model=CustomerList)
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: CustomerService = Depends(get_customer_service),
):
    items, total = await service.list_customers(skip=skip, limit=limit)
    return CustomerList(items=items, total=total)


@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(
    customer_id: uuid.UUID,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.get_customer(customer_id)


@router.patch("/{customer_id}", response_model=CustomerRead)
async def update_customer(
    customer_id: uuid.UUID,
    payload: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.update_customer(customer_id, payload)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: uuid.UUID,
    service: CustomerService = Depends(get_customer_service),
):
    await service.delete_customer(customer_id)
