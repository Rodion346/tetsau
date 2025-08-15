from uuid import UUID
from pydantic import BaseModel


class Role(BaseModel):
    id: UUID
    name: str
    description: str | None = None


class Permission(BaseModel):
    id: UUID
    name: str
    description: str | None = None


class AssignRole(BaseModel):
    user_id: UUID
    role_id: UUID
