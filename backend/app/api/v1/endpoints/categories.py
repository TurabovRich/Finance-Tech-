from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.v1.schemas.categories import CategoryRead
from app.core.deps import DbSession, get_current_user_id
from app.services.category_service import CategoryService

router = APIRouter()


@router.get("", response_model=list[CategoryRead])
async def list_categories(
    db: DbSession, user_id: str = Depends(get_current_user_id)
) -> list[CategoryRead]:
    return await CategoryService(db).list_categories(UUID(user_id))
