"""Document business logic — Phase 6."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.repositories.case_repository import CaseRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.document import DocumentCreate, DocumentUpdate


class DocumentService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = DocumentRepository(session)
        self._cases = CaseRepository(session)
        self._users = UserRepository(session)

    async def _validate_case(self, case_id: uuid.UUID) -> None:
        case = await self._cases.get_by_id(case_id)
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found",
            )

    async def _validate_uploader(self, user_id: uuid.UUID) -> None:
        user = await self._users.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Uploader user not found",
            )

    async def create_document(self, data: DocumentCreate) -> Document:
        await self._validate_case(data.case_id)
        if data.uploaded_by:
            await self._validate_uploader(data.uploaded_by)
        
        existing = await self._repo.get_by_external_reference(data.external_reference)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="External reference already exists",
            )
        
        document = Document(
            external_reference=data.external_reference,
            case_id=data.case_id,
            document_type=data.document_type,
            file_name=data.file_name,
            file_size=data.file_size,
            file_hash=data.file_hash,
            uploaded_by=data.uploaded_by,
        )
        return await self._repo.add(document)

    async def get_document(self, document_id: uuid.UUID) -> Document:
        document = await self._repo.get_by_id(document_id)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )
        return document

    async def list_documents(
        self,
        *,
        case_id: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Document], int]:
        documents = await self._repo.list_documents(
            case_id=case_id,
            skip=skip,
            limit=limit,
        )
        total = await self._repo.count(case_id=case_id)
        return documents, total

    async def update_document(
        self,
        document_id: uuid.UUID,
        data: DocumentUpdate,
    ) -> Document:
        document = await self.get_document(document_id)
        
        if data.external_reference and data.external_reference != document.external_reference:
            existing = await self._repo.get_by_external_reference(data.external_reference)
            if existing and existing.id != document_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="External reference already exists",
                )
            document.external_reference = data.external_reference
        
        if data.document_type is not None:
            document.document_type = data.document_type
        if data.file_name:
            document.file_name = data.file_name
        if data.file_size is not None:
            document.file_size = data.file_size
        if data.file_hash:
            document.file_hash = data.file_hash
        
        return await self._repo.update(document)

    async def delete_document(self, document_id: uuid.UUID) -> None:
        await self.get_document(document_id)
        await self._repo.delete(document_id)
