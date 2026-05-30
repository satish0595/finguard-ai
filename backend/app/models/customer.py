"""Customer ORM model — Phase 2 (monitored entity, not app user)."""

import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CustomerType(str, enum.Enum):
    INDIVIDUAL = "individual"
    BUSINESS = "business"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


class CustomerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING_REVIEW = "pending_review"
    CLOSED = "closed"


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    external_reference: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )
    legal_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    customer_type: Mapped[CustomerType] = mapped_column(
        Enum(CustomerType, name="customer_type", native_enum=False),
        default=CustomerType.INDIVIDUAL,
    )
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level", native_enum=False),
        default=RiskLevel.UNKNOWN,
    )
    status: Mapped[CustomerStatus] = mapped_column(
        Enum(CustomerStatus, name="customer_status", native_enum=False),
        default=CustomerStatus.ACTIVE,
    )
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
