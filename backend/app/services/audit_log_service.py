"""AuditLog business logic — Phase 7."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditAction, AuditLog, EntityType
from app.repositories.audit_log_repository import AuditLogRepository
from app.schemas.audit_log import AuditLogCreate


class AuditLogService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = AuditLogRepository(session)

    async def create_audit_log(self, data: AuditLogCreate) -> AuditLog:
        """Create and persist an audit log entry."""
        audit_log = AuditLog(
            entity_type=data.entity_type,
            entity_id=data.entity_id,
            action=data.action,
            performed_by=data.performed_by,
            old_values=data.old_values,
            new_values=data.new_values,
        )
        return await self._repo.add(audit_log)

    async def list_audit_logs(
        self,
        *,
        entity_type: EntityType | None = None,
        entity_id: uuid.UUID | None = None,
        performed_by: uuid.UUID | None = None,
        action: AuditAction | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[AuditLog], int]:
        """List audit logs with optional filtering."""
        logs = await self._repo.list_audit_logs(
            entity_type=entity_type,
            entity_id=entity_id,
            performed_by=performed_by,
            action=action,
            skip=skip,
            limit=limit,
        )
        total = await self._repo.count(
            entity_type=entity_type,
            entity_id=entity_id,
            performed_by=performed_by,
            action=action,
        )
        return logs, total
