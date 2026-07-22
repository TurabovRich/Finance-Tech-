import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
REFRESH_TOKEN_BYTES = 32


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str, extra: dict[str, Any] | None = None) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # jti guarantees each issued token is unique even if issued within the same
    # second (e.g. login immediately followed by refresh) — without it, two
    # tokens with identical sub/exp/type/sid claims sign to the same JWT string.
    payload = {"sub": subject, "exp": expire, "type": "access", "jti": secrets.token_hex(8)}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def generate_refresh_token() -> str:
    """Opaque, high-entropy refresh token. Not a JWT — the server never re-derives
    it, only compares hashes, so it can be revoked by deleting/flagging its row."""
    return secrets.token_urlsafe(REFRESH_TOKEN_BYTES)


def hash_token(token: str) -> str:
    """One-way digest used to look up/store refresh tokens without persisting the raw value."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
