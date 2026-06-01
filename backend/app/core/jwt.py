from datetime import datetime, timedelta
from typing import Any

from jose import jwt, JWTError

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(data: dict[str, Any], expires_delta: int | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=(expires_delta or settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
