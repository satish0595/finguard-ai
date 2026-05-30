"""Alert Pydantic schemas — Phase 4."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.alert import AlertSeverity, AlertStatus, AlertType


class AlertBase(BaseModel):
    external_reference: str = Field(min_length=1, max_length=64)
    customer_id: uuid.UUID
    transaction_id: uuid.UUID | None = None
    assigned_to: uuid.UUID | None = None
    alert_type: AlertType
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.OPEN
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    triggered_at: datetime
    resolved_at: datetime | None = None


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    external_reference: str | None = Field(default=None, min_length=1, max_length=64)
    transaction_id: uuid.UUID | None = None
    assigned_to: uuid.UUID | None = None
    alert_type: AlertType | None = None
    severity: AlertSeverity | None = None
    status: AlertStatus | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    triggered_at: datetime | None = None
    resolved_at: datetime | None = None


class AlertRead(AlertBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class AlertList(BaseModel):
    items: list[AlertRead]
    total: int
