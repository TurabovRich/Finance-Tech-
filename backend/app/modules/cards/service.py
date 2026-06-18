from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cards.models import LinkedCard
from app.modules.cards.repository import CardRepository
from app.modules.cards.schemas import CardCreate, CardRead


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
