from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.v1.schemas.cards import CardCreate, CardRead
from app.core.deps import DbSession, get_current_user_id
from app.services.card_service import CardService

router = APIRouter()


@router.get("", response_model=list[CardRead])
async def list_cards(db: DbSession, user_id: str = Depends(get_current_user_id)) -> list[CardRead]:
    return await CardService(db).list_cards(UUID(user_id))


@router.post("", response_model=CardRead, status_code=status.HTTP_201_CREATED)
async def link_card(
    data: CardCreate, db: DbSession, user_id: str = Depends(get_current_user_id)
) -> CardRead:
    return await CardService(db).link_card(UUID(user_id), data)
