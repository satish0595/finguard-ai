"""Case API routes — Phase 5."""

import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_case_service
from app.models.case import CaseStatus
from app.schemas.case import CaseCreate, CaseList, CaseRead, CaseUpdate
from app.services.case_service import CaseService

router = APIRouter(prefix="/cases", tags=["cases"])


@router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
async def create_case(
    payload: CaseCreate,
    service: CaseService = Depends(get_case_service),
):
    return await service.create_case(payload)


@router.get("", response_model=CaseList)
async def list_cases(
    customer_id: uuid.UUID | None = None,
    status: CaseStatus | None = None,
    assigned_to: uuid.UUID | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: CaseService = Depends(get_case_service),
):
    items, total = await service.list_cases(
        customer_id=customer_id,
        status=status,
        assigned_to=assigned_to,
        skip=skip,
        limit=limit,
    )
    return CaseList(items=items, total=total)


@router.get("/{case_id}", response_model=CaseRead)
async def get_case(
    case_id: uuid.UUID,
    service: CaseService = Depends(get_case_service),
):
    return await service.get_case(case_id)


@router.patch("/{case_id}", response_model=CaseRead)
async def update_case(
    case_id: uuid.UUID,
    payload: CaseUpdate,
    service: CaseService = Depends(get_case_service),
):
    return await service.update_case(case_id, payload)


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(
    case_id: uuid.UUID,
    service: CaseService = Depends(get_case_service),
):
    await service.delete_case(case_id)
