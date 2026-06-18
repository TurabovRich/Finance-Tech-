from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.models import Category


class CategoryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_for_user(self, user_id: UUID) -> list[Category]:
        result = await self.db.execute(
            select(Category).where(or_(Category.is_system.is_(True), Category.user_id == user_id))
        )
        return list(result.scalars().all())
