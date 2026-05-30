"""User API routes — Phase 1."""

import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_user_service
from app.schemas.user import UserCreate, UserList, UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = await service.create_user(payload)
    return user


@router.get("", response_model=UserList)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: UserService = Depends(get_user_service),
):
    items, total = await service.list_users(skip=skip, limit=limit)
    return UserList(items=items, total=total)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
):
    return await service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    return await service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
):
    await service.delete_user(user_id)
