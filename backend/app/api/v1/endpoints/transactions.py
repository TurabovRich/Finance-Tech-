from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.api.v1.schemas.transactions import TransactionFilter, TransactionRead
from app.core.deps import DbSession
from app.services.transaction_service import TransactionService

router = APIRouter()


@router.get("", response_model=list[TransactionRead])
async def list_transactions(
    db: DbSession,
    user_id: UUID | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    category_id: UUID | None = None,
) -> list[TransactionRead]:
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not wired yet")
    filters = TransactionFilter(limit=limit, offset=offset, category_id=category_id)
    return await TransactionService(db).list_transactions(user_id, filters)


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    transaction_id: UUID, db: DbSession, user_id: UUID | None = None
) -> TransactionRead:
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not wired yet")
    tx = await TransactionService(db).get_transaction(user_id, transaction_id)
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return tx
