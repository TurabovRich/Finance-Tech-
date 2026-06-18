from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.cards.models import CardNetwork


class CardCreate(BaseModel):
    network: CardNetwork
    last_four: str = Field(..., min_length=4, max_length=4)
    bank_name: str | None = None
    nickname: str | None = None
    is_primary: bool = False


class CardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    network: CardNetwork
    last_four: str
    bank_name: str | None
    nickname: str | None
    is_primary: bool
    created_at: datetime
