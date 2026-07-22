from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OTPRequest(BaseModel):
    phone: str = Field(..., examples=["+998901234567"])


class OTPVerify(BaseModel):
    phone: str
    code: str = Field(..., min_length=4, max_length=6)
    device_name: str | None = Field(default=None, max_length=120, examples=["iPhone 14 Pro"])


class PINSetup(BaseModel):
    pin: str = Field(..., min_length=4, max_length=6)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LogoutRequest(BaseModel):
    refresh_token: str


class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    device_name: str | None
    ip_address: str | None
    created_at: datetime
    last_used_at: datetime
    expires_at: datetime
    is_current: bool = False
