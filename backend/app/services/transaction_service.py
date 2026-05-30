"""Transaction business logic — Phase 3."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.repositories.customer_repository import CustomerRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = TransactionRepository(session)
        self._customers = CustomerRepository(session)

    async def _ensure_customer(self, customer_id: uuid.UUID) -> None:
        if not await self._customers.exists(customer_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

    async def create_transaction(self, data: TransactionCreate) -> Transaction:
        await self._ensure_customer(data.customer_id)
        existing = await self._repo.get_by_external_reference(data.external_reference)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="External reference already exists",
            )
        transaction = Transaction(
            customer_id=data.customer_id,
            external_reference=data.external_reference,
            amount=data.amount,
            currency=data.currency.upper(),
            transaction_type=data.transaction_type,
            direction=data.direction,
            status=data.status,
            description=data.description,
            counterparty_name=data.counterparty_name,
            transaction_at=data.transaction_at,
        )
        return await self._repo.add(transaction)

    async def get_transaction(self, transaction_id: uuid.UUID) -> Transaction:
        transaction = await self._repo.get_by_id(transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
        return transaction

    async def list_transactions(
        self,
        *,
        customer_id: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Transaction], int]:
        if customer_id is not None:
            await self._ensure_customer(customer_id)
        items = await self._repo.list_transactions(
            customer_id=customer_id, skip=skip, limit=limit
        )
        total = await self._repo.count(customer_id=customer_id)
        return items, total

    async def update_transaction(
        self, transaction_id: uuid.UUID, data: TransactionUpdate
    ) -> Transaction:
        transaction = await self.get_transaction(transaction_id)
        if (
            data.external_reference
            and data.external_reference != transaction.external_reference
        ):
            existing = await self._repo.get_by_external_reference(
                data.external_reference
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="External reference already exists",
                )
            transaction.external_reference = data.external_reference
        if data.amount is not None:
            transaction.amount = data.amount
        if data.currency is not None:
            transaction.currency = data.currency.upper()
        if data.transaction_type is not None:
            transaction.transaction_type = data.transaction_type
        if data.direction is not None:
            transaction.direction = data.direction
        if data.status is not None:
            transaction.status = data.status
        if data.description is not None:
            transaction.description = data.description
        if data.counterparty_name is not None:
            transaction.counterparty_name = data.counterparty_name
        if data.transaction_at is not None:
            transaction.transaction_at = data.transaction_at
        return await self._repo.update(transaction)

    async def delete_transaction(self, transaction_id: uuid.UUID) -> None:
        transaction = await self.get_transaction(transaction_id)
        await self._repo.delete(transaction)
