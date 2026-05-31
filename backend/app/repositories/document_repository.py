"""Document data access — Phase 6."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, document: Document) -> Document:
        self._session.add(document)
        await self._session.commit()
        await self._session.refresh(document)
        return document

    async def get_by_id(self, document_id: uuid.UUID) -> Document | None:
        return await self._session.get(Document, document_id)

    async def get_by_external_reference(self, external_reference: str) -> Document | None:
        result = await self._session.execute(
            select(Document).where(Document.external_reference == external_reference)
        )
        return result.scalar_one_or_none()

    async def list_documents(
        self,
        *,
        case_id: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Document]:
        stmt = select(Document).order_by(Document.uploaded_at.desc())
        if case_id is not None:
            stmt = stmt.where(Document.case_id == case_id)
        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self,
        *,
        case_id: uuid.UUID | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Document)
        if case_id is not None:
            stmt = stmt.where(Document.case_id == case_id)
        result = await self._session.execute(stmt)
        return int(result.scalar_one())

    async def update(self, document: Document) -> Document:
        await self._session.commit()
        await self._session.refresh(document)
        return document

    async def delete(self, document_id: uuid.UUID) -> None:
        document = await self.get_by_id(document_id)
        if document:
            await self._session.delete(document)
            await self._session.commit()

    async def exists(self, document_id: uuid.UUID) -> bool:
        result = await self._session.execute(
            select(func.exists().where(Document.id == document_id))
        )
        return bool(result.scalar())
