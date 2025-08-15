from uuid import UUID

from sqlalchemy import select

from .base import BaseRepository
from ..models.permission import Role, Permission, RolePermission, UserRole


class PermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=Permission)

    async def user_has_permission(self, user_id: UUID, permission_name: str) -> bool:
        async with self.db() as session:
            query = (
                select(Permission)
                .join(RolePermission, RolePermission.permission_id == Permission.id)
                .join(Role, Role.id == RolePermission.role_id)
                .join(UserRole, UserRole.role_id == Role.id)
                .where(UserRole.user_id == user_id, Permission.name == permission_name)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None

    async def list_roles(self):
        async with self.db() as session:
            result = await session.execute(select(Role))
            return result.scalars().all()

    async def list_permissions(self):
        async with self.db() as session:
            result = await session.execute(select(Permission))
            return result.scalars().all()

    async def assign_role_to_user(self, user_id: UUID, role_id: UUID) -> bool:
        async with self.db() as session:
            session.add(UserRole(user_id=user_id, role_id=role_id))
            await session.commit()
            return True

    async def ensure_defaults(self) -> None:
        async with self.db() as session:
            roles = await session.execute(select(Role))
            if not roles.scalars().first():
                admin = Role(name="admin", description="Administrator")
                user = Role(name="user", description="Regular user")
                session.add_all([admin, user])
                await session.flush()
                read = Permission(name="items:read", description="Read items")
                create = Permission(name="items:create", description="Create items")
                session.add_all([read, create])
                await session.flush()
                session.add_all(
                    [
                        RolePermission(role_id=admin.id, permission_id=read.id),
                        RolePermission(role_id=admin.id, permission_id=create.id),
                        RolePermission(role_id=user.id, permission_id=read.id),
                    ]
                )
                await session.commit()
