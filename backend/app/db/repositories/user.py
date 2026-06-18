from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, phone: str, full_name: str | None = None, locale: str = "uz") -> User:
        """Create and persist a new User instance.
        Caller must ensure phone uniqueness (handled by DB constraint)."""
        user = User(phone=phone, full_name=full_name, locale=locale)
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_phone(self, phone: str) -> User | None:
        result = await self.db.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()
