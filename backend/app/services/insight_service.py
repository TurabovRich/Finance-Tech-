from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.insights import CategorySpend, MonthlyInsight
from app.db.repositories.insight import InsightRepository


class InsightService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = InsightRepository(db)

    async def monthly_summary(self, user_id: UUID, month: str | None = None) -> MonthlyInsight:
        target = datetime.strptime(month, "%Y-%m").replace(tzinfo=UTC) if month else datetime.now(UTC)
        rows = await self.repo.spending_by_category(user_id, target)
        total = sum(int(amount) for _, _, amount in rows)
        by_category = [
            CategorySpend(
                category_id=str(cat_id) if cat_id else None,
                category_name=name or "Uncategorized",
                amount=int(amount),
                percentage=round((int(amount) / total * 100) if total else 0, 1),
            )
            for cat_id, name, amount in rows
        ]
        return MonthlyInsight(
            month=target.strftime("%Y-%m"),
            total_spent=total,
            total_income=0,
            by_category=by_category,
        )
