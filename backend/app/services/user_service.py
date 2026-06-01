"""User business logic — Phase 1."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.core.security import verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserRepository(session)

    async def create_user(self, data: UserCreate) -> User:
        existing = await self._repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
            is_active=data.is_active,
        )
        return await self._repo.add(user)

    async def get_user(self, user_id: uuid.UUID) -> User:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def list_users(self, *, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        items = await self._repo.list_users(skip=skip, limit=limit)
        total = await self._repo.count()
        return items, total

    async def update_user(self, user_id: uuid.UUID, data: UserUpdate) -> User:
        user = await self.get_user(user_id)
        if data.email and data.email != user.email:
            existing = await self._repo.get_by_email(data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered",
                )
            user.email = data.email
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.role is not None:
            user.role = data.role
        if data.is_active is not None:
            user.is_active = data.is_active
        if data.password:
            user.hashed_password = hash_password(data.password)
        return await self._repo.update(user)

    async def delete_user(self, user_id: uuid.UUID) -> None:
        user = await self.get_user(user_id)
        await self._repo.delete(user)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self._repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
