"""PolicyChunk API routes — Phase 8."""

import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_policy_chunk_service
from app.schemas.policy_chunk import (
    PolicyChunkCreate,
    PolicyChunkList,
    PolicyChunkRead,
    PolicyChunkUpdate,
)
from app.services.policy_chunk_service import PolicyChunkService

router = APIRouter(prefix="/policy-chunks", tags=["policy-chunks"])


@router.post("", response_model=PolicyChunkRead, status_code=status.HTTP_201_CREATED)
async def create_policy_chunk(
    payload: PolicyChunkCreate,
    service: PolicyChunkService = Depends(get_policy_chunk_service),
):
    return await service.create_policy_chunk(payload)


@router.get("", response_model=PolicyChunkList)
async def list_policy_chunks(
    policy_name: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: PolicyChunkService = Depends(get_policy_chunk_service),
):
    items, total = await service.list_policy_chunks(
        policy_name=policy_name,
        skip=skip,
        limit=limit,
    )
    return PolicyChunkList(items=items, total=total)


@router.get("/{policy_chunk_id}", response_model=PolicyChunkRead)
async def get_policy_chunk(
    policy_chunk_id: uuid.UUID,
    service: PolicyChunkService = Depends(get_policy_chunk_service),
):
    return await service.get_policy_chunk(policy_chunk_id)


@router.patch("/{policy_chunk_id}", response_model=PolicyChunkRead)
async def update_policy_chunk(
    policy_chunk_id: uuid.UUID,
    payload: PolicyChunkUpdate,
    service: PolicyChunkService = Depends(get_policy_chunk_service),
):
    return await service.update_policy_chunk(policy_chunk_id, payload)


@router.delete("/{policy_chunk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy_chunk(
    policy_chunk_id: uuid.UUID,
    service: PolicyChunkService = Depends(get_policy_chunk_service),
):
    await service.delete_policy_chunk(policy_chunk_id)
