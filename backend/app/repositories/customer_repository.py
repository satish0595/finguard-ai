"""Customer data access — Phase 2."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, customer_id: uuid.UUID) -> Customer | None:
        return await self._session.get(Customer, customer_id)

    async def exists(self, customer_id: uuid.UUID) -> bool:
        customer = await self.get_by_id(customer_id)
        return customer is not None

    async def get_by_external_reference(self, external_reference: str) -> Customer | None:
        result = await self._session.execute(
            select(Customer).where(Customer.external_reference == external_reference)
        )
        return result.scalar_one_or_none()

    async def list_customers(
        self, *, skip: int = 0, limit: int = 100
    ) -> list[Customer]:
        result = await self._session.execute(
            select(Customer)
            .order_by(Customer.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(Customer)
        )
        return int(result.scalar_one())

    async def add(self, customer: Customer) -> Customer:
        self._session.add(customer)
        await self._session.commit()
        await self._session.refresh(customer)
        return customer

    async def update(self, customer: Customer) -> Customer:
        await self._session.commit()
        await self._session.refresh(customer)
        return customer

    async def delete(self, customer: Customer) -> None:
        await self._session.delete(customer)
        await self._session.commit()
