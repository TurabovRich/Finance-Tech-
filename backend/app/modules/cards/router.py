from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.deps import DbSession
from app.modules.cards.schemas import CardCreate, CardRead
from app.modules.cards.service import CardService

router = APIRouter()


@router.get("", response_model=list[CardRead])
async def list_cards(db: DbSession, user_id: UUID | None = None) -> list[CardRead]:
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not wired yet")
    return await CardService(db).list_cards(user_id)


@router.post("", response_model=CardRead, status_code=status.HTTP_201_CREATED)
async def link_card(data: CardCreate, db: DbSession, user_id: UUID | None = None) -> CardRead:
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not wired yet")
    return await CardService(db).link_card(user_id, data)
