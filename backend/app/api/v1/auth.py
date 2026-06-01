from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer

from app.api.deps import get_user_service
from app.core.jwt import create_access_token, decode_access_token
from app.services.user_service import UserService
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    svc: UserService = Depends(get_user_service),
):
    user = await svc.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}


bearer = HTTPBearer()


@router.post("/refresh")
async def refresh_token(
    creds: HTTPAuthorizationCredentials = Security(bearer),
    svc: UserService = Depends(get_user_service),
):
    payload = decode_access_token(creds.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    sub = payload.get("sub")
    try:
        user_id = uuid.UUID(sub)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")
    user = await svc.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    new_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": new_token, "token_type": "bearer"}
