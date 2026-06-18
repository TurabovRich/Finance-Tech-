from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.cards import CardCreate, CardRead
from app.db.repositories.card import CardRepository
from app.models.card import LinkedCard


class CardService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = CardRepository(db)

    async def list_cards(self, user_id: UUID) -> list[CardRead]:
        cards = await self.repo.list_by_user(user_id)
        return [CardRead.model_validate(c) for c in cards]

    async def link_card(self, user_id: UUID, data: CardCreate) -> CardRead:
        card = LinkedCard(user_id=user_id, **data.model_dump())
        created = await self.repo.create(card)
        return CardRead.model_validate(created)
