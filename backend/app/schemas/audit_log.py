"""AuditLog Pydantic schemas — Phase 7."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.audit_log import AuditAction, EntityType


class AuditLogBase(BaseModel):
    entity_type: EntityType
    entity_id: uuid.UUID
    action: AuditAction
    performed_by: uuid.UUID | None = None
    old_values: dict[str, Any] | None = None
    new_values: dict[str, Any] | None = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogRead(AuditLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    performed_at: datetime
    created_at: datetime


class AuditLogList(BaseModel):
    items: list[AuditLogRead]
    total: int
