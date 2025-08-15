# app/api/v1/auth/manager.py
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Request
from pydantic import EmailStr
from uuid import UUID

from app.core.config import settings
from app.core.repositories.user import UserRepository
from app.schemas.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthManager:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    # Пароли
    async def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    # Только access JWT
    async def create_access_token(self, sub: str, minutes: int = 60) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": sub,
            "typ": "access",
            "jti": str(uuid4()),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=minutes)).timestamp()),
        }
        auth = settings.get_auth_data()
        return jwt.encode(payload, auth["secret_key"], algorithm=auth["algorithm"])

    async def get_user_from_bearer(self, token: str) -> User:
        if not token:
            raise HTTPException(status_code=401, detail="Token required")
        try:
            auth = settings.get_auth_data()
            payload = jwt.decode(token, auth["secret_key"], algorithms=[auth["algorithm"]])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        if payload.get("typ") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        exp = payload.get("exp")
        if not exp or datetime.fromtimestamp(int(exp), tz=timezone.utc) <= datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")

        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Missing sub")

        user = await self._user_repo.get_by_id_or_none(UUID(sub))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        if not user.is_active:
            raise HTTPException(status_code=401, detail="Inactive user")

        return user
