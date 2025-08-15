# app/api/depence.py (обновлённое)
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.repositories.user import UserRepository
from app.services.user import UserService
from app.services.room import RoomService
from app.core.repositories.room import RoomRepository
from app.api.v1.auth.manager import AuthManager

bearer_scheme = HTTPBearer(auto_error=True)

async def get_user_service() -> UserService:
    return UserService(UserRepository())

async def get_room_service() -> RoomService:
    return RoomService(RoomRepository())

async def get_auth_manager() -> AuthManager:
    return AuthManager(UserRepository())

async def get_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
                   auth: AuthManager = Depends(get_auth_manager)):
    token = credentials.credentials
    return await auth.get_user_from_bearer(token)

async def get_moderator(user = Depends(get_user)):
    if getattr(user, "is_admin", False) or getattr(user, "is_moderator", False):
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет прав")

async def get_admin(user = Depends(get_user)):
    if getattr(user, "is_admin", False):
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет прав")
