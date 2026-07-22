from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import AuthSession


class SessionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, session: AuthSession) -> AuthSession:
        self.db.add(session)
        await self.db.flush()
        return session

    async def get_by_token_hash(self, token_hash: str) -> AuthSession | None:
        result = await self.db.execute(
            select(AuthSession).where(AuthSession.refresh_token_hash == token_hash)
        )
        return result.scalar_one_or_none()

    async def get_by_id_for_user(self, session_id: UUID, user_id: UUID) -> AuthSession | None:
        result = await self.db.execute(
            select(AuthSession).where(AuthSession.id == session_id, AuthSession.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_active_for_user(self, user_id: UUID, now: datetime) -> list[AuthSession]:
        result = await self.db.execute(
            select(AuthSession)
            .where(
                AuthSession.user_id == user_id,
                AuthSession.revoked_at.is_(None),
                AuthSession.expires_at > now,
            )
            .order_by(AuthSession.last_used_at.desc())
        )
        return list(result.scalars().all())

    async def touch(self, session: AuthSession, now: datetime) -> None:
        session.last_used_at = now
        await self.db.flush()

    async def revoke(self, session: AuthSession, now: datetime) -> None:
        session.revoked_at = now
        await self.db.flush()
