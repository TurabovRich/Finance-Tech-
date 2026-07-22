from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.auth import OTPRequest, OTPVerify, PINSetup, TokenResponse
from app.core.security import create_access_token, hash_password
from app.db.repositories.auth import AuthRepository


class AuthService:
    """Auth service. OTP delivery stubbed in development until SMS provider is integrated."""

    def __init__(self, db: AsyncSession) -> None:
        self.repo = AuthRepository(db)

    async def request_otp(self, data: OTPRequest) -> dict[str, str]:
        await self.repo.get_or_create_by_phone(data.phone)
        # TODO: send OTP via SMS provider (Eskiz, Playmobile, etc.)
        return {"message": "OTP sent", "hint": "Use 123456 in development"}

    async def verify_otp(self, data: OTPVerify) -> TokenResponse:
        if data.code != "123456":
            raise ValueError("Invalid OTP")
        user = await self.repo.get_or_create_by_phone(data.phone)
        token = create_access_token(str(user.id))
        return TokenResponse(access_token=token)

    async def setup_pin(self, user_id: str, data: PINSetup) -> dict[str, str]:
        # TODO: persist pin_hash on user
        _ = hash_password(data.pin)
        return {"message": "PIN configured"}
