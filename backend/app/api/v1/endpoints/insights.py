from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.v1.schemas.insights import MonthlyInsight
from app.core.deps import DbSession, get_current_user_id
from app.services.insight_service import InsightService

router = APIRouter()


@router.get("/monthly", response_model=MonthlyInsight)
async def monthly_insights(
    db: DbSession,
    user_id: str = Depends(get_current_user_id),
    month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
) -> MonthlyInsight:
    return await InsightService(db).monthly_summary(UUID(user_id), month)
