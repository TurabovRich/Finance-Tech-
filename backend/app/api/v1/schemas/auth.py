from pydantic import BaseModel, Field


class OTPRequest(BaseModel):
    phone: str = Field(..., examples=["+998901234567"])


class OTPVerify(BaseModel):
    phone: str
    code: str = Field(..., min_length=4, max_length=6)


class PINSetup(BaseModel):
    pin: str = Field(..., min_length=4, max_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
