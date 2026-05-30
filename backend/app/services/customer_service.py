"""Customer business logic — Phase 2."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = CustomerRepository(session)

    async def create_customer(self, data: CustomerCreate) -> Customer:
        existing = await self._repo.get_by_external_reference(data.external_reference)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="External reference already exists",
            )
        customer = Customer(
            external_reference=data.external_reference,
            legal_name=data.legal_name,
            email=data.email,
            phone=data.phone,
            customer_type=data.customer_type,
            risk_level=data.risk_level,
            status=data.status,
            country_code=data.country_code,
            date_of_birth=data.date_of_birth,
        )
        return await self._repo.add(customer)

    async def get_customer(self, customer_id: uuid.UUID) -> Customer:
        customer = await self._repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )
        return customer

    async def list_customers(
        self, *, skip: int = 0, limit: int = 100
    ) -> tuple[list[Customer], int]:
        items = await self._repo.list_customers(skip=skip, limit=limit)
        total = await self._repo.count()
        return items, total

    async def update_customer(
        self, customer_id: uuid.UUID, data: CustomerUpdate
    ) -> Customer:
        customer = await self.get_customer(customer_id)
        if (
            data.external_reference
            and data.external_reference != customer.external_reference
        ):
            existing = await self._repo.get_by_external_reference(
                data.external_reference
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="External reference already exists",
                )
            customer.external_reference = data.external_reference
        if data.legal_name is not None:
            customer.legal_name = data.legal_name
        if data.email is not None:
            customer.email = data.email
        if data.phone is not None:
            customer.phone = data.phone
        if data.customer_type is not None:
            customer.customer_type = data.customer_type
        if data.risk_level is not None:
            customer.risk_level = data.risk_level
        if data.status is not None:
            customer.status = data.status
        if data.country_code is not None:
            customer.country_code = data.country_code
        if data.date_of_birth is not None:
            customer.date_of_birth = data.date_of_birth
        return await self._repo.update(customer)

    async def delete_customer(self, customer_id: uuid.UUID) -> None:
        customer = await self.get_customer(customer_id)
        await self._repo.delete(customer)
