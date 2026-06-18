from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cards.models import LinkedCard


class CardRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_by_user(self, user_id: UUID) -> list[LinkedCard]:
        result = await self.db.execute(
            select(LinkedCard).where(LinkedCard.user_id == user_id).order_by(LinkedCard.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(self, card: LinkedCard) -> LinkedCard:
        self.db.add(card)
        await self.db.flush()
        return card
