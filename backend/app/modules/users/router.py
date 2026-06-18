from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.deps import DbSession
from app.modules.users.schemas import UserRead, UserUpdate
from app.modules.users.service import UserService

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_me(db: DbSession, user_id: UUID | None = None) -> UserRead:
    # TODO: replace with authenticated user from JWT dependency
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not wired yet")
    profile = await UserService(db).get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return profile


@router.patch("/me", response_model=UserRead)
async def update_me(data: UserUpdate, db: DbSession, user_id: UUID | None = None) -> UserRead:
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not wired yet")
    profile = await UserService(db).update_profile(user_id, data)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return profile
