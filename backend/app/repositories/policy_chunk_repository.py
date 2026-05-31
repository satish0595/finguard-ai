"""PolicyChunk data access — Phase 8."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.policy_chunk import PolicyChunk


class PolicyChunkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, policy_chunk: PolicyChunk) -> PolicyChunk:
        self._session.add(policy_chunk)
        await self._session.commit()
        await self._session.refresh(policy_chunk)
        return policy_chunk

    async def get_by_id(self, policy_chunk_id: uuid.UUID) -> PolicyChunk | None:
        return await self._session.get(PolicyChunk, policy_chunk_id)

    async def get_by_external_reference(
        self, external_reference: str
    ) -> PolicyChunk | None:
        result = await self._session.execute(
            select(PolicyChunk).where(
                PolicyChunk.external_reference == external_reference
            )
        )
        return result.scalar_one_or_none()

    async def list_policy_chunks(
        self,
        *,
        policy_name: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[PolicyChunk]:
        stmt = select(PolicyChunk).order_by(PolicyChunk.policy_name, PolicyChunk.chunk_index)
        if policy_name is not None:
            stmt = stmt.where(PolicyChunk.policy_name == policy_name)
        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self,
        *,
        policy_name: str | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(PolicyChunk)
        if policy_name is not None:
            stmt = stmt.where(PolicyChunk.policy_name == policy_name)
        result = await self._session.execute(stmt)
        return int(result.scalar_one())

    async def update(self, policy_chunk: PolicyChunk) -> PolicyChunk:
        await self._session.commit()
        await self._session.refresh(policy_chunk)
        return policy_chunk

    async def delete(self, policy_chunk_id: uuid.UUID) -> None:
        policy_chunk = await self.get_by_id(policy_chunk_id)
        if policy_chunk:
            await self._session.delete(policy_chunk)
            await self._session.commit()
