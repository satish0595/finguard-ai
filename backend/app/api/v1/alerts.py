"""Alert API routes — Phase 4."""

import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_alert_service
from app.models.alert import AlertStatus
from app.schemas.alert import AlertCreate, AlertList, AlertRead, AlertUpdate
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
async def create_alert(
    payload: AlertCreate,
    service: AlertService = Depends(get_alert_service),
):
    return await service.create_alert(payload)


@router.get("", response_model=AlertList)
async def list_alerts(
    customer_id: uuid.UUID | None = None,
    status: AlertStatus | None = None,
    assigned_to: uuid.UUID | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: AlertService = Depends(get_alert_service),
):
    items, total = await service.list_alerts(
        customer_id=customer_id,
        status=status,
        assigned_to=assigned_to,
        skip=skip,
        limit=limit,
    )
    return AlertList(items=items, total=total)


@router.get("/{alert_id}", response_model=AlertRead)
async def get_alert(
    alert_id: uuid.UUID,
    service: AlertService = Depends(get_alert_service),
):
    return await service.get_alert(alert_id)


@router.patch("/{alert_id}", response_model=AlertRead)
async def update_alert(
    alert_id: uuid.UUID,
    payload: AlertUpdate,
    service: AlertService = Depends(get_alert_service),
):
    return await service.update_alert(alert_id, payload)


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: uuid.UUID,
    service: AlertService = Depends(get_alert_service),
):
    await service.delete_alert(alert_id)
