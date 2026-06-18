from fastapi import APIRouter, HTTPException, status

from app.core.deps import DbSession
from app.modules.auth.schemas import OTPRequest, OTPVerify, PINSetup, TokenResponse
from app.modules.auth.service import AuthService

router = APIRouter()


@router.post("/otp/request")
async def request_otp(data: OTPRequest, db: DbSession) -> dict[str, str]:
    return await AuthService(db).request_otp(data)


@router.post("/otp/verify", response_model=TokenResponse)
async def verify_otp(data: OTPVerify, db: DbSession) -> TokenResponse:
    try:
        return await AuthService(db).verify_otp(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/pin/setup")
async def setup_pin(data: PINSetup, db: DbSession) -> dict[str, str]:
    # TODO: wire current user from JWT dependency
    return await AuthService(db).setup_pin("pending", data)
