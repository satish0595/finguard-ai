"""Document API routes — Phase 6."""

import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_document_service
from app.schemas.document import DocumentCreate, DocumentList, DocumentRead, DocumentUpdate
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def create_document(
    payload: DocumentCreate,
    service: DocumentService = Depends(get_document_service),
):
    return await service.create_document(payload)


@router.get("", response_model=DocumentList)
async def list_documents(
    case_id: uuid.UUID | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: DocumentService = Depends(get_document_service),
):
    items, total = await service.list_documents(
        case_id=case_id,
        skip=skip,
        limit=limit,
    )
    return DocumentList(items=items, total=total)


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(
    document_id: uuid.UUID,
    service: DocumentService = Depends(get_document_service),
):
    return await service.get_document(document_id)


@router.patch("/{document_id}", response_model=DocumentRead)
async def update_document(
    document_id: uuid.UUID,
    payload: DocumentUpdate,
    service: DocumentService = Depends(get_document_service),
):
    return await service.update_document(document_id, payload)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: uuid.UUID,
    service: DocumentService = Depends(get_document_service),
):
    await service.delete_document(document_id)
