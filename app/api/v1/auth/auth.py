import random
from asyncio import to_thread

from fastapi import APIRouter, Depends, HTTPException, status, Response, BackgroundTasks
from jose import jwt
from pydantic import EmailStr
from app.api.v1.auth.manager import AuthManager
from app.api.depence import (
    get_user_service,
    get_auth_manager,
    get_user,
    update_refresh_token,
)
from app.core.config import settings
from app.schemas.user import (
    LoginUser,
    User,
    CreateUser,
    ResponseLoginUser,
    UpdateUserToken,
    UpdatePasswordUser,
    UpdateUserProfile,
)
from app.services.user import UserService



router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: CreateUser,
    response: Response,
    task: BackgroundTasks,
    auth_manager: AuthManager = Depends(get_auth_manager),
    user_service: UserService = Depends(get_user_service),
) -> User | None:
    user = await user_service.get_user_by_email(user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )
    user_data.hashed_password = await auth_manager.get_password_hash(
        password=user_data.hashed_password
    )
    user = await user_service.create_user(user_data)
    access_token = await auth_manager.create_access_token(str(user.id))

    # Установка cookies с правильными параметрами для локальной разработки
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        httponly=True,
        samesite="none",  # Важно: только "None" позволяет кросс-доменные куки
        secure=True,  # Обязательно для SameSite=None
    )
    return user


@router.post("/login", response_model=ResponseLoginUser)
async def login(
    user_data: LoginUser,
    response: Response,
    task: BackgroundTasks,
    auth_manager: AuthManager = Depends(get_auth_manager),
    user_service: UserService = Depends(get_user_service),
) -> ResponseLoginUser:
    user = await user_service.get_user_by_email(user_data.email)
    if (
        not user
        or not user.is_active
        or not await auth_manager.verify_password(user_data.password, user.hashed_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверная почта или пароль",
        )
    access_token = await auth_manager.create_access_token(str(user.id))
    refresh_token = await auth_manager.create_refresh_token(str(user.id))
    await user_service.update_refresh_token_by_id(
        UpdateUserToken(id=user.id, refresh_token=refresh_token)
    )

    # Установка cookies с правильными параметрами для локальной разработки
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        httponly=True,
        samesite="none",  # Важно: только "None" позволяет кросс-доменные куки
        secure=True,  # Обязательно для SameSite=None
    )

    return ResponseLoginUser(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/refresh-token", response_model=ResponseLoginUser, status_code=status.HTTP_200_OK
)
async def refresh_token(tokens: ResponseLoginUser = Depends(update_refresh_token)):
    return tokens


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    response: Response,
    user_data: User = Depends(get_user),
    user_service: UserService = Depends(get_user_service),
):
    response.delete_cookie(key="users_access_token", httponly=True)
    await user_service.update_refresh_token_by_id(
        UpdateUserToken(id=user_data.id, refresh_token=None)
    )
    return {"message": "Пользователь успешно вышел из системы"}


@router.get("/me", response_model=User)
async def read_me(user: User = Depends(get_user)):
    return user


@router.put("/me", response_model=User)
async def update_me(
    user_update: UpdateUserProfile,
    user: User = Depends(get_user),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_user_profile(user.id, user_update)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    response: Response,
    user: User = Depends(get_user),
    user_service: UserService = Depends(get_user_service),
):
    await user_service.deactivate_user(user.id)
    response.delete_cookie(key="users_access_token", httponly=True)
    await user_service.update_refresh_token_by_id(
        UpdateUserToken(id=user.id, refresh_token=None)
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
