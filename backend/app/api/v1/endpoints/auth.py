from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.v1.schemas.auth import (
    AccessTokenResponse,
    LogoutRequest,
    OTPRequest,
    OTPVerify,
    PINSetup,
    RefreshRequest,
    SessionRead,
    TokenResponse,
)
from app.core.deps import DbSession, get_current_session_id, get_current_user_id
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/otp/request")
async def request_otp(data: OTPRequest, db: DbSession) -> dict[str, str]:
    return await AuthService(db).request_otp(data)


@router.post("/otp/verify", response_model=TokenResponse)
async def verify_otp(data: OTPVerify, request: Request, db: DbSession) -> TokenResponse:
    try:
        return await AuthService(db).verify_otp(
            data,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(data: RefreshRequest, db: DbSession) -> AccessTokenResponse:
    try:
        return await AuthService(db).refresh(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(data: LogoutRequest, db: DbSession) -> None:
    # Possession of the refresh token is the proof of ownership here — no separate
    # access-token auth is required, since the access token may already be expired.
    await AuthService(db).logout(data.refresh_token)


@router.get("/sessions", response_model=list[SessionRead])
async def list_sessions(
    db: DbSession,
    user_id: str = Depends(get_current_user_id),
    current_session_id: str | None = Depends(get_current_session_id),
) -> list[SessionRead]:
    return await AuthService(db).list_sessions(UUID(user_id), current_session_id)


@router.post("/sessions/{session_id}/revoke", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_session(
    session_id: UUID, db: DbSession, user_id: str = Depends(get_current_user_id)
) -> None:
    try:
        await AuthService(db).revoke_session(session_id, UUID(user_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/pin/setup")
async def setup_pin(data: PINSetup, db: DbSession, user_id: str = Depends(get_current_user_id)) -> dict[str, str]:
    return await AuthService(db).setup_pin(user_id, data)
