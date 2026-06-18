from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user import UserRepository
from app.models.user import User


class AuthRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.users = UserRepository(db)
        self.db = db

    async def get_or_create_by_phone(self, phone: str) -> User:
        user = await self.users.get_by_phone(phone)
        if user:
            return user
        user = User(phone=phone)
        self.db.add(user)
        await self.db.flush()
        return user
