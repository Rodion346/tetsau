from datetime import datetime
from os import supports_fd
from uuid import UUID

from app.core.repositories.user import UserRepository
from app.schemas.user import CreateUser, User, UpdateUserToken, UpdateUserProfile

from pydantic import EmailStr


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def create_user(self, user: CreateUser) -> User:
        stmt = await self._user_repo.add_user(user)
        return stmt

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self._user_repo.get_by_id_or_none(user_id)
        return user

    async def get_user_by_tg_username(self, tg_username: str) -> User:
        user = await self._user_repo.get_user_by_tg_username(tg_username)
        return user

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        user = await self._user_repo.get_user_by_email_or_none(email)
        return user

    async def update_refresh_token_by_id(self, user: UpdateUserToken) -> bool:
        stmt = await self._user_repo.update_refresh_token_by_id(user)
        return stmt

    async def update_email_status_by_id(self, user: User) -> bool:
        stmt = await self._user_repo.update_email_status_by_id(user)
        return stmt

    async def update_password_by_id(self, user: User, password: str) -> bool:
        stmt = await self._user_repo.update_password_by_id(user, password)
        return stmt

    async def update_user_profile(self, user_id: UUID, data: UpdateUserProfile) -> User:
        stmt = await self._user_repo.update_user_profile(user_id, data)
        return stmt

    async def deactivate_user(self, user_id: UUID) -> bool:
        stmt = await self._user_repo.deactivate_user(user_id)
        return stmt

    async def update_session_time_by_id(
        self, user_id: UUID, new_session_time: int
    ) -> bool:
        stmt = await self._user_repo.update_session_time_by_id(
            user_id, new_session_time
        )
        return stmt

    async def update_expire_plan_by_id(
        self, user_id: UUID, expire_plan: datetime
    ) -> bool:
        stmt = await self._user_repo.update_expire_plan_by_id(user_id, expire_plan)
        return stmt

    async def update_trial_room_by_id(
        self, user_id: UUID, trial_started_room_id: UUID
    ) -> bool:
        stmt = await self._user_repo.update_trial_room_by_id(
            user_id, trial_started_room_id
        )
        return stmt

    async def get_support(self) -> list:
        supports = await self._user_repo.get_support()
        return supports
