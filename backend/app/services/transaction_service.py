from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.transactions import TransactionFilter, TransactionRead
from app.db.repositories.transaction import TransactionRepository


class TransactionService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = TransactionRepository(db)

    async def list_transactions(self, user_id: UUID, filters: TransactionFilter) -> list[TransactionRead]:
        rows = await self.repo.list_by_user(
            user_id,
            limit=filters.limit,
            offset=filters.offset,
            category_id=filters.category_id,
        )
        return [TransactionRead.model_validate(row) for row in rows]

    async def get_transaction(self, user_id: UUID, transaction_id: UUID) -> TransactionRead | None:
        row = await self.repo.get_by_id(transaction_id, user_id)
        return TransactionRead.model_validate(row) if row else None
