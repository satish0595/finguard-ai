"""Document Pydantic schemas — Phase 6."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.document import DocumentType


class DocumentBase(BaseModel):
    external_reference: str = Field(min_length=1, max_length=64)
    case_id: uuid.UUID
    document_type: DocumentType
    file_name: str = Field(min_length=1, max_length=255)
    file_size: int = Field(ge=1)
    file_hash: str = Field(min_length=1, max_length=64)
    uploaded_by: uuid.UUID | None = None


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    external_reference: str | None = Field(default=None, min_length=1, max_length=64)
    document_type: DocumentType | None = None
    file_name: str | None = Field(default=None, min_length=1, max_length=255)
    file_size: int | None = Field(default=None, ge=1)
    file_hash: str | None = Field(default=None, min_length=1, max_length=64)


class DocumentRead(DocumentBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime


class DocumentList(BaseModel):
    items: list[DocumentRead]
    total: int
