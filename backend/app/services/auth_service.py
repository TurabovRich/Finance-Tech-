import logging
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.auth import (
    AccessTokenResponse,
    OTPRequest,
    OTPVerify,
    PINSetup,
    RefreshRequest,
    SessionRead,
    TokenResponse,
)
from app.core.config import settings
from app.core.security import create_access_token, generate_refresh_token, hash_password, hash_token
from app.db.repositories.auth import AuthRepository
from app.db.repositories.session import SessionRepository
from app.models.session import AuthSession

logger = logging.getLogger("app.auth")


class AuthService:
    """Auth service. OTP delivery stubbed in development until SMS provider is integrated."""

    def __init__(self, db: AsyncSession) -> None:
        self.repo = AuthRepository(db)
        self.sessions = SessionRepository(db)

    async def request_otp(self, data: OTPRequest) -> dict[str, str]:
        await self.repo.get_or_create_by_phone(data.phone)
        # TODO: send OTP via SMS provider (Eskiz, Playmobile, etc.)
        return {"message": "OTP sent", "hint": "Use 123456 in development"}

    async def verify_otp(
        self,
        data: OTPVerify,
        *,
        ip_address: str | None,
        user_agent: str | None,
    ) -> TokenResponse:
        if data.code != "123456":
            raise ValueError("Invalid OTP")
        user = await self.repo.get_or_create_by_phone(data.phone)

        now = datetime.now(UTC)
        raw_token = generate_refresh_token()
        session = AuthSession(
            user_id=user.id,
            refresh_token_hash=hash_token(raw_token),
            device_name=data.device_name,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        await self.sessions.create(session)
        logger.info("session created user_id=%s session_id=%s", user.id, session.id)

        access_token = create_access_token(str(user.id), extra={"sid": str(session.id)})
        return TokenResponse(access_token=access_token, refresh_token=raw_token)

    async def refresh(self, data: RefreshRequest) -> AccessTokenResponse:
        now = datetime.now(UTC)
        session = await self.sessions.get_by_token_hash(hash_token(data.refresh_token))
        if session is None or session.revoked_at is not None or session.expires_at <= now:
            logger.warning("refresh rejected: invalid, expired, or revoked token")
            raise ValueError("Invalid refresh token")

        await self.sessions.touch(session, now)
        access_token = create_access_token(str(session.user_id), extra={"sid": str(session.id)})
        logger.info("session refreshed user_id=%s session_id=%s", session.user_id, session.id)
        return AccessTokenResponse(access_token=access_token)

    async def logout(self, refresh_token: str) -> None:
        session = await self.sessions.get_by_token_hash(hash_token(refresh_token))
        if session is None or session.revoked_at is not None:
            # Already gone/revoked — logout is idempotent, nothing to do.
            return
        await self.sessions.revoke(session, datetime.now(UTC))
        logger.info("session revoked via logout user_id=%s session_id=%s", session.user_id, session.id)

    async def list_sessions(self, user_id: UUID, current_session_id: str | None) -> list[SessionRead]:
        sessions = await self.sessions.list_active_for_user(user_id, datetime.now(UTC))
        return [
            SessionRead(
                id=s.id,
                device_name=s.device_name,
                ip_address=s.ip_address,
                created_at=s.created_at,
                last_used_at=s.last_used_at,
                expires_at=s.expires_at,
                is_current=(str(s.id) == current_session_id),
            )
            for s in sessions
        ]

    async def revoke_session(self, session_id: UUID, user_id: UUID) -> None:
        session = await self.sessions.get_by_id_for_user(session_id, user_id)
        if session is None:
            raise ValueError("Session not found")
        await self.sessions.revoke(session, datetime.now(UTC))
        logger.info("session revoked by user user_id=%s session_id=%s", user_id, session_id)

    async def setup_pin(self, user_id: str, data: PINSetup) -> dict[str, str]:
        # TODO: persist pin_hash on user
        _ = hash_password(data.pin)
        return {"message": "PIN configured"}
