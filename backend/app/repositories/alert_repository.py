"""Alert data access — Phase 4."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert, AlertStatus


class AlertRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, alert_id: uuid.UUID) -> Alert | None:
        return await self._session.get(Alert, alert_id)

    async def get_by_external_reference(self, external_reference: str) -> Alert | None:
        result = await self._session.execute(
            select(Alert).where(Alert.external_reference == external_reference)
        )
        return result.scalar_one_or_none()

    async def list_alerts(
        self,
        *,
        customer_id: uuid.UUID | None = None,
        status: AlertStatus | None = None,
        assigned_to: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Alert]:
        stmt = select(Alert).order_by(Alert.triggered_at.desc())
        if customer_id is not None:
            stmt = stmt.where(Alert.customer_id == customer_id)
        if status is not None:
            stmt = stmt.where(Alert.status == status)
        if assigned_to is not None:
            stmt = stmt.where(Alert.assigned_to == assigned_to)
        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self,
        *,
        customer_id: uuid.UUID | None = None,
        status: AlertStatus | None = None,
        assigned_to: uuid.UUID | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Alert)
        if customer_id is not None:
            stmt = stmt.where(Alert.customer_id == customer_id)
        if status is not None:
            stmt = stmt.where(Alert.status == status)
        if assigned_to is not None:
            stmt = stmt.where(Alert.assigned_to == assigned_to)
        result = await self._session.execute(stmt)
        return int(result.scalar_one())

    async def add(self, alert: Alert) -> Alert:
        self._session.add(alert)
        await self._session.commit()
        await self._session.refresh(alert)
        return alert

    async def update(self, alert: Alert) -> Alert:
        await self._session.commit()
        await self._session.refresh(alert)
        return alert

    async def delete(self, alert: Alert) -> None:
        await self._session.delete(alert)
        await self._session.commit()
