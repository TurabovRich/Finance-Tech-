from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.transactions.models import TransactionStatus, TransactionType


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    card_id: UUID | None
    category_id: UUID | None
    type: TransactionType
    status: TransactionStatus
    amount: int
    fee: int
    currency: str
    merchant: str | None
    description: str | None
    occurred_at: datetime


class TransactionFilter(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    category_id: UUID | None = None
