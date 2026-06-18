from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas.categories import CategoryRead
from app.core.deps import DbSession
from app.services.category_service import CategoryService

router = APIRouter()


@router.get("", response_model=list[CategoryRead])
async def list_categories(db: DbSession, user_id: UUID | None = None) -> list[CategoryRead]:
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not wired yet")
    return await CategoryService(db).list_categories(user_id)
