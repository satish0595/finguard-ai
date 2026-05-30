"""Case business logic — Phase 5."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case, CaseStatus
from app.repositories.alert_repository import AlertRepository
from app.repositories.case_repository import CaseRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.user_repository import UserRepository
from app.schemas.case import CaseCreate, CaseUpdate


class CaseService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = CaseRepository(session)
        self._customers = CustomerRepository(session)
        self._alerts = AlertRepository(session)
        self._users = UserRepository(session)

    async def _validate_customer(self, customer_id: uuid.UUID) -> None:
        if not await self._customers.exists(customer_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

    async def _validate_alert(self, customer_id: uuid.UUID, alert_id: uuid.UUID) -> None:
        alert = await self._alerts.get_by_id(alert_id)
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found",
            )
        if alert.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Alert does not belong to customer",
            )

    async def _validate_assignee(self, user_id: uuid.UUID) -> None:
        user = await self._users.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found",
            )

    async def create_case(self, data: CaseCreate) -> Case:
        await self._validate_customer(data.customer_id)
        if data.alert_id:
            await self._validate_alert(data.customer_id, data.alert_id)
        if data.assigned_to:
            await self._validate_assignee(data.assigned_to)
        existing = await self._repo.get_by_external_reference(data.external_reference)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="External reference already exists",
            )
        case = Case(
            external_reference=data.external_reference,
            customer_id=data.customer_id,
            alert_id=data.alert_id,
            assigned_to=data.assigned_to,
            priority=data.priority,
            status=data.status,
            title=data.title,
            summary=data.summary,
            opened_at=data.opened_at,
            closed_at=data.closed_at,
        )
        return await self._repo.add(case)

    async def get_case(self, case_id: uuid.UUID) -> Case:
        case = await self._repo.get_by_id(case_id)
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found",
            )
        return case

    async def list_cases(
        self,
        *,
        customer_id: uuid.UUID | None = None,
        status: CaseStatus | None = None,
        assigned_to: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Case], int]:
        if customer_id is not None:
            await self._validate_customer(customer_id)
        if assigned_to is not None:
            await self._validate_assignee(assigned_to)
        items = await self._repo.list_cases(
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

    async def update_case(self, case_id: uuid.UUID, data: CaseUpdate) -> Case:
        case = await self.get_case(case_id)
        if (
            data.external_reference
            and data.external_reference != case.external_reference
        ):
            existing = await self._repo.get_by_external_reference(
                data.external_reference
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="External reference already exists",
                )
            case.external_reference = data.external_reference
        if data.alert_id is not None:
            await self._validate_alert(case.customer_id, data.alert_id)
            case.alert_id = data.alert_id
        if data.assigned_to is not None:
            await self._validate_assignee(data.assigned_to)
            case.assigned_to = data.assigned_to
        if data.priority is not None:
            case.priority = data.priority
        if data.status is not None:
            case.status = data.status
        if data.title is not None:
            case.title = data.title
        if data.summary is not None:
            case.summary = data.summary
        if data.opened_at is not None:
            case.opened_at = data.opened_at
        if data.closed_at is not None:
            case.closed_at = data.closed_at
        return await self._repo.update(case)

    async def delete_case(self, case_id: uuid.UUID) -> None:
        case = await self.get_case(case_id)
        await self._repo.delete(case)
