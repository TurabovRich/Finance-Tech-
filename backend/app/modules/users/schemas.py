from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    phone: str
    full_name: str | None
    locale: str
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = None
    locale: str | None = None
