"""Alert business logic — Phase 4."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert, AlertStatus
from app.repositories.alert_repository import AlertRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.alert import AlertCreate, AlertUpdate


class AlertService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = AlertRepository(session)
        self._customers = CustomerRepository(session)
        self._transactions = TransactionRepository(session)
        self._users = UserRepository(session)

    async def _validate_customer(self, customer_id: uuid.UUID) -> None:
        if not await self._customers.exists(customer_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

    async def _validate_transaction(
        self, customer_id: uuid.UUID, transaction_id: uuid.UUID
    ) -> None:
        transaction = await self._transactions.get_by_id(transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
        if transaction.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction does not belong to customer",
            )

    async def _validate_assignee(self, user_id: uuid.UUID) -> None:
        user = await self._users.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found",
            )

    async def create_alert(self, data: AlertCreate) -> Alert:
        await self._validate_customer(data.customer_id)
        if data.transaction_id:
            await self._validate_transaction(data.customer_id, data.transaction_id)
        if data.assigned_to:
            await self._validate_assignee(data.assigned_to)
        existing = await self._repo.get_by_external_reference(data.external_reference)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="External reference already exists",
            )
        alert = Alert(
            external_reference=data.external_reference,
            customer_id=data.customer_id,
            transaction_id=data.transaction_id,
            assigned_to=data.assigned_to,
            alert_type=data.alert_type,
            severity=data.severity,
            status=data.status,
            title=data.title,
            description=data.description,
            triggered_at=data.triggered_at,
            resolved_at=data.resolved_at,
        )
        return await self._repo.add(alert)

    async def get_alert(self, alert_id: uuid.UUID) -> Alert:
        alert = await self._repo.get_by_id(alert_id)
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found",
            )
        return alert

    async def list_alerts(
        self,
        *,
        customer_id: uuid.UUID | None = None,
        status: AlertStatus | None = None,
        assigned_to: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Alert], int]:
        if customer_id is not None:
            await self._validate_customer(customer_id)
        if assigned_to is not None:
            await self._validate_assignee(assigned_to)
        items = await self._repo.list_alerts(
            customer_id=customer_id,
            status=status,
            assigned_to=assigned_to,
            skip=skip,
            limit=limit,
        )
        total = await self._repo.count(
            customer_id=customer_id,
            status=status,
            assigned_to=assigned_to,
        )
        return items, total

    async def update_alert(self, alert_id: uuid.UUID, data: AlertUpdate) -> Alert:
        alert = await self.get_alert(alert_id)
        if (
            data.external_reference
            and data.external_reference != alert.external_reference
        ):
            existing = await self._repo.get_by_external_reference(
                data.external_reference
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="External reference already exists",
                )
            alert.external_reference = data.external_reference
        if data.transaction_id is not None:
            await self._validate_transaction(alert.customer_id, data.transaction_id)
            alert.transaction_id = data.transaction_id
        if data.assigned_to is not None:
            await self._validate_assignee(data.assigned_to)
            alert.assigned_to = data.assigned_to
        if data.alert_type is not None:
            alert.alert_type = data.alert_type
        if data.severity is not None:
            alert.severity = data.severity
        if data.status is not None:
            alert.status = data.status
        if data.title is not None:
            alert.title = data.title
        if data.description is not None:
            alert.description = data.description
        if data.triggered_at is not None:
            alert.triggered_at = data.triggered_at
        if data.resolved_at is not None:
            alert.resolved_at = data.resolved_at
        return await self._repo.update(alert)

    async def delete_alert(self, alert_id: uuid.UUID) -> None:
        alert = await self.get_alert(alert_id)
        await self._repo.delete(alert)
