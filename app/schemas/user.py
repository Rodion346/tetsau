import enum
import re
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum


class LanguageLevel(str, enum.Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class User(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: Optional[str]
    level: int = 0
    is_active: bool
    is_active_email: bool
    is_admin: bool
    is_moderator: bool
    created_at: datetime
    updated_at: datetime


class CreateUser(BaseModel):
    email: EmailStr
    hashed_password: str = Field(..., alias="password")
    first_name: str
    last_name: Optional[str]

    @validator("hashed_password")
    def validate_password(cls, value):
        # Проверка длины пароля
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Проверка наличия хотя бы одной цифры
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        # Проверка наличия хотя бы одной заглавной буквы
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        return value


class UpdatePasswordUser(BaseModel):
    email: EmailStr
    new_password: str

    @validator("new_password")
    def validate_password(cls, value):
        # Проверка длины пароля
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Проверка наличия хотя бы одной цифры
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        # Проверка наличия хотя бы одной заглавной буквы
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        return value


class UserProfile(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: Optional[str]
    language_level: Optional[LanguageLevel]
    total_session_time: int
    telegram_username: Optional[str]


class UpdateUserProfile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_level: Optional[LanguageLevel] = None
    telegram_username: Optional[str] = None


class ResponseLoginUser(BaseModel):
    access_token: str
    refresh_token: Optional[str]


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class UpdateUserToken(BaseModel):
    id: UUID
    refresh_token: Optional[str]


class WeeklyActivity(BaseModel):
    active: int = 0
    language_level: Optional[LanguageLevel] = None


class ActivityForTheYear(BaseModel):
    january: list[WeeklyActivity]
    february: list[WeeklyActivity]
    march: list[WeeklyActivity]
    april: list[WeeklyActivity]
    may: list[WeeklyActivity]
    june: list[WeeklyActivity]
    july: list[WeeklyActivity]
    august: list[WeeklyActivity]
    september: list[WeeklyActivity]
    october: list[WeeklyActivity]
    november: list[WeeklyActivity]
    december: list[WeeklyActivity]
    streak: int = 0
    percent: int = 0
    level: int = 0
