import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class CardNetwork(str, enum.Enum):
    HUMO = "humo"
    UZCARD = "uzcard"
    VISA = "visa"


class LinkedCard(Base):
    __tablename__ = "cards"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    network: Mapped[CardNetwork] = mapped_column(Enum(CardNetwork), nullable=False)
    last_four: Mapped[str] = mapped_column(String(4), nullable=False)
    bank_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    nickname: Mapped[str | None] = mapped_column(String(60), nullable=True)
    is_primary: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
