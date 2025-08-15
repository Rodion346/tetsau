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
