from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.categories import CategoryRead
from app.db.repositories.category import CategoryRepository


class CategoryService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = CategoryRepository(db)

    async def list_categories(self, user_id: UUID) -> list[CategoryRead]:
        rows = await self.repo.list_for_user(user_id)
        return [CategoryRead.model_validate(row) for row in rows]
