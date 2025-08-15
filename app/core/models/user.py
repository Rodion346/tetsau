from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import BOOLEAN, UUID, TIMESTAMP
from sqlalchemy import String, ForeignKey, Enum
from pydantic import EmailStr
from datetime import datetime

from .base import Base
from ...schemas.user import LanguageLevel


class User(Base):
    email: Mapped[EmailStr] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str]
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[int] = mapped_column(nullable=False, default=0)
    is_active_email: Mapped[bool] = mapped_column(BOOLEAN, default=False, nullable=True)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    is_moderator: Mapped[bool] = mapped_column(BOOLEAN, default=False, nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)

    language_level: Mapped[LanguageLevel] = mapped_column(
        Enum(
            LanguageLevel,
        ),
        nullable=True,
        default=None,
    )
    total_session_time: Mapped[int] = mapped_column(
        default=0, nullable=False
    )  # in minutes
    telegram_username: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[str] = mapped_column(nullable=True)
    expire_plan: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    trial_started_room_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
