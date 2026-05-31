"""PolicyChunk Pydantic schemas — Phase 8."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PolicyChunkBase(BaseModel):
    external_reference: str = Field(min_length=1, max_length=64)
    policy_name: str = Field(min_length=1, max_length=255)
    chunk_index: int = Field(ge=0)
    content: str = Field(min_length=1)
    tags: list[str] | None = None


class PolicyChunkCreate(PolicyChunkBase):
    pass


class PolicyChunkUpdate(BaseModel):
    external_reference: str | None = Field(default=None, min_length=1, max_length=64)
    policy_name: str | None = Field(default=None, min_length=1, max_length=255)
    chunk_index: int | None = Field(default=None, ge=0)
    content: str | None = Field(default=None, min_length=1)
    tags: list[str] | None = None


class PolicyChunkRead(PolicyChunkBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PolicyChunkList(BaseModel):
    items: list[PolicyChunkRead]
    total: int
