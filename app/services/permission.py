from uuid import UUID

from app.core.repositories.permission import PermissionRepository


class PermissionService:
    def __init__(self, repo: PermissionRepository):
        self._repo = repo

    async def user_has_permission(self, user_id: UUID, permission_name: str) -> bool:
        return await self._repo.user_has_permission(user_id, permission_name)

    async def list_roles(self):
        return await self._repo.list_roles()

    async def list_permissions(self):
        return await self._repo.list_permissions()

    async def assign_role(self, user_id: UUID, role_id: UUID) -> bool:
        return await self._repo.assign_role_to_user(user_id, role_id)

    async def ensure_defaults(self) -> None:
        await self._repo.ensure_defaults()
