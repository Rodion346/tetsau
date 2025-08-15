# app/api/depence.py (обновлённое)
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.repositories.user import UserRepository
from app.core.repositories.permission import PermissionRepository
from app.services.user import UserService
from app.services.permission import PermissionService
from app.api.v1.auth.manager import AuthManager
from app.schemas.user import UpdateUserToken, ResponseLoginUser
from jose import jwt, JWTError
from uuid import UUID
from app.core.config import settings
from datetime import datetime, timezone

bearer_scheme = HTTPBearer(auto_error=True)


async def get_user_service() -> UserService:
    return UserService(UserRepository())


async def get_permission_service() -> PermissionService:
    return PermissionService(PermissionRepository())


async def get_auth_manager() -> AuthManager:
    return AuthManager(UserRepository())


async def get_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth: AuthManager = Depends(get_auth_manager),
):
    token = credentials.credentials
    return await auth.get_user_from_bearer(token)


async def get_moderator(user=Depends(get_user)):
    if getattr(user, "is_admin", False) or getattr(user, "is_moderator", False):
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет прав")


async def get_admin(user=Depends(get_user)):
    if getattr(user, "is_admin", False):
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет прав")


async def update_refresh_token(
    request: Request,
    user_service: UserService = Depends(get_user_service),
    auth: AuthManager = Depends(get_auth_manager),
) -> ResponseLoginUser:
    data = await request.json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token required")
    auth_data = settings.get_auth_data()
    try:
        payload = jwt.decode(
            refresh_token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]]
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if payload.get("typ") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    exp = payload.get("exp")
    if not exp or datetime.fromtimestamp(int(exp), tz=timezone.utc) <= datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    if payload.get("sub") is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = UUID(payload.get("sub"))
    user = await user_service.get_user_by_id(user_id)
    if not user or user.refresh_token != refresh_token or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    access_token = await auth.create_access_token(str(user.id))
    new_refresh = await auth.create_refresh_token(str(user.id))
    await user_service.update_refresh_token_by_id(
        UpdateUserToken(id=user.id, refresh_token=new_refresh)
    )
    return ResponseLoginUser(access_token=access_token, refresh_token=new_refresh)
