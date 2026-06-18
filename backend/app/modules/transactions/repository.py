from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.transactions.models import Transaction


class TransactionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_by_user(
        self,
        user_id: UUID,
        *,
        limit: int = 20,
        offset: int = 0,
        category_id: UUID | None = None,
    ) -> list[Transaction]:
        query = select(Transaction).where(Transaction.user_id == user_id)
        if category_id:
            query = query.where(Transaction.category_id == category_id)
        query = query.order_by(Transaction.occurred_at.desc()).limit(limit).offset(offset)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, transaction_id: UUID, user_id: UUID) -> Transaction | None:
        result = await self.db.execute(
            select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == user_id)
        )
        return result.scalar_one_or_none()
