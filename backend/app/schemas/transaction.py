"""Transaction Pydantic schemas — Phase 3."""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.transaction import (
    TransactionDirection,
    TransactionStatus,
    TransactionType,
)


class TransactionBase(BaseModel):
    customer_id: uuid.UUID
    external_reference: str = Field(min_length=1, max_length=64)
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    transaction_type: TransactionType
    direction: TransactionDirection
    status: TransactionStatus = TransactionStatus.PENDING
    description: str | None = None
    counterparty_name: str | None = Field(default=None, max_length=255)
    transaction_at: datetime


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    external_reference: str | None = Field(default=None, min_length=1, max_length=64)
    amount: Decimal | None = Field(default=None, gt=0, max_digits=18, decimal_places=2)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    transaction_type: TransactionType | None = None
    direction: TransactionDirection | None = None
    status: TransactionStatus | None = None
    description: str | None = None
    counterparty_name: str | None = Field(default=None, max_length=255)
    transaction_at: datetime | None = None


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TransactionList(BaseModel):
    items: list[TransactionRead]
    total: int
