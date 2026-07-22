from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import get_db

DbSession = Annotated[AsyncSession, Depends(get_db)]


def _decode_bearer_token(authorization: str | None) -> dict:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


async def get_current_user_id(authorization: Annotated[str | None, Header()] = None) -> str:
    payload = _decode_bearer_token(authorization)
    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing sub claim")
    return user_id


async def get_current_session_id(authorization: Annotated[str | None, Header()] = None) -> str | None:
    """Best-effort session id embedded in the access token (`sid` claim), used only to
    flag which session is "current" in session-list responses. Never used for authz."""
    payload = _decode_bearer_token(authorization)
    return payload.get("sid")
