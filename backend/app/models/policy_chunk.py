"""PolicyChunk ORM model — Phase 8 (policy management)."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, JSON, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PolicyChunk(Base):
    __tablename__ = "policy_chunks"

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
    policy_name: Mapped[str] = mapped_column(
        String(255),
        index=True,
    )
    chunk_index: Mapped[int] = mapped_column(
        Integer,
        index=True,
    )
    content: Mapped[str] = mapped_column(Text)
    tags: Mapped[list[str] | None] = mapped_column(
        JSON,
        default=None,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
