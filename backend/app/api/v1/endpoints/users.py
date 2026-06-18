from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.schemas.users import UserRead, UserUpdate
from app.core.deps import DbSession, get_current_user_id
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_me(db: DbSession, user_id: str = Depends(get_current_user_id)) -> UserRead:
    profile = await UserService(db).get_profile(UUID(user_id))
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return profile


@router.patch("/me", response_model=UserRead)
async def update_me(data: UserUpdate, db: DbSession, user_id: str = Depends(get_current_user_id)) -> UserRead:
    profile = await UserService(db).update_profile(UUID(user_id), data)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return profile
