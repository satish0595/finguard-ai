"""AuditLog data access — Phase 7."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditAction, AuditLog, EntityType


class AuditLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, audit_log: AuditLog) -> AuditLog:
        self._session.add(audit_log)
        await self._session.commit()
        await self._session.refresh(audit_log)
        return audit_log

    async def get_by_id(self, audit_log_id: uuid.UUID) -> AuditLog | None:
        return await self._session.get(AuditLog, audit_log_id)

    async def list_audit_logs(
        self,
        *,
        entity_type: EntityType | None = None,
        entity_id: uuid.UUID | None = None,
        performed_by: uuid.UUID | None = None,
        action: AuditAction | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditLog]:
        stmt = select(AuditLog).order_by(AuditLog.performed_at.desc())
        if entity_type is not None:
            stmt = stmt.where(AuditLog.entity_type == entity_type)
        if entity_id is not None:
            stmt = stmt.where(AuditLog.entity_id == entity_id)
        if performed_by is not None:
            stmt = stmt.where(AuditLog.performed_by == performed_by)
        if action is not None:
            stmt = stmt.where(AuditLog.action == action)
        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self,
        *,
        entity_type: EntityType | None = None,
        entity_id: uuid.UUID | None = None,
        performed_by: uuid.UUID | None = None,
        action: AuditAction | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(AuditLog)
        if entity_type is not None:
            stmt = stmt.where(AuditLog.entity_type == entity_type)
        if entity_id is not None:
            stmt = stmt.where(AuditLog.entity_id == entity_id)
        if performed_by is not None:
            stmt = stmt.where(AuditLog.performed_by == performed_by)
        if action is not None:
            stmt = stmt.where(AuditLog.action == action)
        result = await self._session.execute(stmt)
        return int(result.scalar_one())
