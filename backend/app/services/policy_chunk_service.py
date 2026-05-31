"""PolicyChunk business logic — Phase 8."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.policy_chunk import PolicyChunk
from app.repositories.policy_chunk_repository import PolicyChunkRepository
from app.schemas.policy_chunk import PolicyChunkCreate, PolicyChunkUpdate


class PolicyChunkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = PolicyChunkRepository(session)

    async def create_policy_chunk(self, data: PolicyChunkCreate) -> PolicyChunk:
        existing = await self._repo.get_by_external_reference(data.external_reference)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="External reference already exists",
            )

        policy_chunk = PolicyChunk(
            external_reference=data.external_reference,
            policy_name=data.policy_name,
            chunk_index=data.chunk_index,
            content=data.content,
            tags=data.tags,
        )
        return await self._repo.add(policy_chunk)

    async def get_policy_chunk(self, policy_chunk_id: uuid.UUID) -> PolicyChunk:
        policy_chunk = await self._repo.get_by_id(policy_chunk_id)
        if not policy_chunk:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy chunk not found",
            )
        return policy_chunk

    async def list_policy_chunks(
        self,
        *,
        policy_name: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[PolicyChunk], int]:
        chunks = await self._repo.list_policy_chunks(
            policy_name=policy_name,
            skip=skip,
            limit=limit,
        )
        total = await self._repo.count(policy_name=policy_name)
        return chunks, total

    async def update_policy_chunk(
        self,
        policy_chunk_id: uuid.UUID,
        data: PolicyChunkUpdate,
    ) -> PolicyChunk:
        policy_chunk = await self.get_policy_chunk(policy_chunk_id)

        if (
            data.external_reference
            and data.external_reference != policy_chunk.external_reference
        ):
            existing = await self._repo.get_by_external_reference(
                data.external_reference
            )
            if existing and existing.id != policy_chunk_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="External reference already exists",
                )
            policy_chunk.external_reference = data.external_reference

        if data.policy_name:
            policy_chunk.policy_name = data.policy_name
        if data.chunk_index is not None:
            policy_chunk.chunk_index = data.chunk_index
        if data.content:
            policy_chunk.content = data.content
        if data.tags is not None:
            policy_chunk.tags = data.tags

        return await self._repo.update(policy_chunk)

    async def delete_policy_chunk(self, policy_chunk_id: uuid.UUID) -> None:
        await self.get_policy_chunk(policy_chunk_id)
        await self._repo.delete(policy_chunk_id)
