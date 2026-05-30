"""Customer Pydantic schemas — Phase 2."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.customer import CustomerStatus, CustomerType, RiskLevel


class CustomerBase(BaseModel):
    external_reference: str = Field(min_length=1, max_length=64)
    legal_name: str = Field(min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=32)
    customer_type: CustomerType = CustomerType.INDIVIDUAL
    risk_level: RiskLevel = RiskLevel.UNKNOWN
    status: CustomerStatus = CustomerStatus.ACTIVE
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    date_of_birth: date | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    external_reference: str | None = Field(default=None, min_length=1, max_length=64)
    legal_name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=32)
    customer_type: CustomerType | None = None
    risk_level: RiskLevel | None = None
    status: CustomerStatus | None = None
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    date_of_birth: date | None = None


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CustomerList(BaseModel):
    items: list[CustomerRead]
    total: int
