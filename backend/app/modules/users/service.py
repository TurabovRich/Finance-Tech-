from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserRead, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = UserRepository(db)

    async def get_profile(self, user_id: UUID) -> UserRead | None:
        user = await self.repo.get_by_id(user_id)
        return UserRead.model_validate(user) if user else None

    async def update_profile(self, user_id: UUID, data: UserUpdate) -> UserRead | None:
        user = await self.repo.get_by_id(user_id)
        if not user:
            return None
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.locale is not None:
            user.locale = data.locale
        return UserRead.model_validate(user)
