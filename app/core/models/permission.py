from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from uuid import UUID

from .base import Base


class Role(Base):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class Permission(Base):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class RolePermission(Base):
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permissions.id"), nullable=False)


class UserRole(Base):
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)
