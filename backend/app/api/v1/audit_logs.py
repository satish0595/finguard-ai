"""AuditLog API routes — Phase 7."""

import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_audit_log_service
from app.models.audit_log import AuditAction, EntityType
from app.schemas.audit_log import AuditLogCreate, AuditLogList, AuditLogRead
from app.services.audit_log_service import AuditLogService

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])


@router.post("", response_model=AuditLogRead, status_code=status.HTTP_201_CREATED)
async def create_audit_log(
    payload: AuditLogCreate,
    service: AuditLogService = Depends(get_audit_log_service),
):
    return await service.create_audit_log(payload)


@router.get("", response_model=AuditLogList)
async def list_audit_logs(
    entity_type: EntityType | None = None,
    entity_id: uuid.UUID | None = None,
    performed_by: uuid.UUID | None = None,
    action: AuditAction | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: AuditLogService = Depends(get_audit_log_service),
):
    items, total = await service.list_audit_logs(
        entity_type=entity_type,
        entity_id=entity_id,
        performed_by=performed_by,
        action=action,
        skip=skip,
        limit=limit,
    )
    return AuditLogList(items=items, total=total)
