"""Case data access — Phase 5."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case, CasePriority, CaseStatus


class CaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, case_id: uuid.UUID) -> Case | None:
        return await self._session.get(Case, case_id)

    async def get_by_external_reference(self, external_reference: str) -> Case | None:
        result = await self._session.execute(
            select(Case).where(Case.external_reference == external_reference)
        )
        return result.scalar_one_or_none()

    async def list_cases(
        self,
        *,
        customer_id: uuid.UUID | None = None,
        status: CaseStatus | None = None,
        assigned_to: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Case]:
        stmt = select(Case).order_by(Case.opened_at.desc())
        if customer_id is not None:
            stmt = stmt.where(Case.customer_id == customer_id)
        if status is not None:
            stmt = stmt.where(Case.status == status)
        if assigned_to is not None:
            stmt = stmt.where(Case.assigned_to == assigned_to)
        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self,
        *,
        customer_id: uuid.UUID | None = None,
        status: CaseStatus | None = None,
        priority: CasePriority | None = None,
        assigned_to: uuid.UUID | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Case)
        if customer_id is not None:
            stmt = stmt.where(Case.customer_id == customer_id)
        if status is not None:
            stmt = stmt.where(Case.status == status)
        if priority is not None:
            stmt = stmt.where(Case.priority == priority)
        if assigned_to is not None:
            stmt = stmt.where(Case.assigned_to == assigned_to)
        result = await self._session.execute(stmt)
        return int(result.scalar_one())

    async def add(self, case: Case) -> Case:
        self._session.add(case)
        await self._session.commit()
        await self._session.refresh(case)
        return case

    async def update(self, case: Case) -> Case:
        await self._session.commit()
        await self._session.refresh(case)
        return case

    async def delete(self, case: Case) -> None:
        await self._session.delete(case)
        await self._session.commit()
