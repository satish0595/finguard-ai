"""Transaction data access — Phase 3."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction, TransactionStatus


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, transaction_id: uuid.UUID) -> Transaction | None:
        return await self._session.get(Transaction, transaction_id)

    async def get_by_external_reference(
        self, external_reference: str
    ) -> Transaction | None:
        result = await self._session.execute(
            select(Transaction).where(
                Transaction.external_reference == external_reference
            )
        )
        return result.scalar_one_or_none()

    async def list_transactions(
        self,
        *,
        customer_id: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Transaction]:
        stmt = select(Transaction).order_by(Transaction.transaction_at.desc())
        if customer_id is not None:
            stmt = stmt.where(Transaction.customer_id == customer_id)
        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self,
        *,
        customer_id: uuid.UUID | None = None,
        status: TransactionStatus | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Transaction)
        if customer_id is not None:
            stmt = stmt.where(Transaction.customer_id == customer_id)
        if status is not None:
            stmt = stmt.where(Transaction.status == status)
        result = await self._session.execute(stmt)
        return int(result.scalar_one())

    async def add(self, transaction: Transaction) -> Transaction:
        self._session.add(transaction)
        await self._session.commit()
        await self._session.refresh(transaction)
        return transaction

    async def update(self, transaction: Transaction) -> Transaction:
        await self._session.commit()
        await self._session.refresh(transaction)
        return transaction

    async def delete(self, transaction: Transaction) -> None:
        await self._session.delete(transaction)
        await self._session.commit()
