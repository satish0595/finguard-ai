"""Case Pydantic schemas — Phase 5."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.case import CasePriority, CaseStatus


class CaseBase(BaseModel):
    external_reference: str = Field(min_length=1, max_length=64)
    customer_id: uuid.UUID
    alert_id: uuid.UUID | None = None
    assigned_to: uuid.UUID | None = None
    priority: CasePriority = CasePriority.MEDIUM
    status: CaseStatus = CaseStatus.OPEN
    title: str = Field(min_length=1, max_length=255)
    summary: str | None = None
    opened_at: datetime
    closed_at: datetime | None = None


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    external_reference: str | None = Field(default=None, min_length=1, max_length=64)
    alert_id: uuid.UUID | None = None
    assigned_to: uuid.UUID | None = None
    priority: CasePriority | None = None
    status: CaseStatus | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    summary: str | None = None
    opened_at: datetime | None = None
    closed_at: datetime | None = None


class CaseRead(CaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CaseList(BaseModel):
    items: list[CaseRead]
    total: int
