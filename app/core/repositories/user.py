from datetime import datetime

from sqlalchemy import select, update, UUID
from pydantic import EmailStr
from .base import BaseRepository
from ..models.user import User
from ...schemas.user import CreateUser, UpdateUserToken


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=User)

    async def add_user(self, user: CreateUser) -> User:
        async with self.db() as session:
            new_user = self.model(**user.dict())
            session.add(new_user)
            await session.commit()
            user = await self.get_user_by_email_or_none(user.email)
            return user

    async def get_user_by_email_or_none(self, email: EmailStr) -> User | None:
        async with self.db() as session:
            query = await session.execute(select(self.model).filter_by(email=email))
            result = query.scalar_one_or_none()
            return result

    async def get_user_by_tg_username(self, tg_username: str) -> User | None:
        async with self.db() as session:
            query = await session.execute(
                select(self.model).filter_by(telegram_username=tg_username)
            )
            result = query.scalar_one_or_none()
            return result

    async def update_refresh_token_by_id(self, user: UpdateUserToken) -> bool:
        async with self.db() as session:
            stmt = await session.execute(
                update(self.model)
                .filter_by(id=user.id)
                .values(refresh_token=user.refresh_token)
            )

            await session.commit()
            return True

    async def update_email_status_by_id(self, user: User) -> bool:
        async with self.db() as session:
            stmt = await session.execute(
                update(self.model).filter_by(id=user.id).values(is_active_email=True)
            )
            await session.commit()
            return True

    async def update_password_by_id(self, user: User, password: str) -> bool:
        async with self.db() as session:
            stmt = await session.execute(
                update(self.model)
                .filter_by(id=user.id)
                .values(hashed_password=password)
            )
            await session.commit()
            return True

    async def update_session_time_by_id(
        self, user_id: UUID, new_session_time: int
    ) -> bool:
        async with self.db() as session:
            stmt = await session.execute(
                update(self.model)
                .filter_by(id=user_id)
                .values(total_session_time=new_session_time)
            )
            await session.commit()
            return True

    async def update_expire_plan_by_id(
        self, user_id: UUID, expire_plan: datetime
    ) -> bool:
        async with self.db() as session:
            stmt = await session.execute(
                update(self.model).filter_by(id=user_id).values(expire_plan=expire_plan)
            )
            await session.commit()
            return True

    async def update_trial_room_by_id(
        self, user_id: UUID, trial_started_room_id: UUID
    ) -> bool:
        async with self.db() as session:
            stmt = await session.execute(
                update(self.model)
                .filter_by(id=user_id)
                .values(trial_started_room_id=trial_started_room_id)
            )
            await session.commit()
            return True

    async def get_support(self) -> list:
        sp_ids = []
        async with self.db() as session:
            supports = select(self.model).filter(
                self.model.is_admin or self.model.is_moderator
            )
            query = await session.execute(supports)
            result = query.scalars().all()
            for user in result:
                if user.telegram_id:
                    sp_ids.append(user.telegram_id)
            return sp_ids
