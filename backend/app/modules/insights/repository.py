from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.models import Category
from app.modules.transactions.models import Transaction, TransactionType


class InsightRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def spending_by_category(self, user_id: UUID, month: datetime) -> list[tuple]:
        start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)

        result = await self.db.execute(
            select(
                Category.id,
                Category.name,
                func.coalesce(func.sum(Transaction.amount), 0),
            )
            .join(Transaction, Transaction.category_id == Category.id, isouter=True)
            .where(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.DEBIT,
                Transaction.occurred_at >= start,
                Transaction.occurred_at < end,
            )
            .group_by(Category.id, Category.name)
        )
        return list(result.all())
