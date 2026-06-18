from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.api.v1.schemas.insights import MonthlyInsight
from app.core.deps import DbSession
from app.services.insight_service import InsightService

router = APIRouter()


@router.get("/monthly", response_model=MonthlyInsight)
async def monthly_insights(
    db: DbSession,
    user_id: UUID | None = None,
    month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
) -> MonthlyInsight:
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not wired yet")
    return await InsightService(db).monthly_summary(user_id, month)
