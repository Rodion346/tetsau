from fastapi import APIRouter, Depends, status

from app.api.depence import get_admin, get_permission_service
from app.schemas.access import AssignRole, Role, Permission
from app.services.permission import PermissionService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/roles", response_model=list[Role], dependencies=[Depends(get_admin)])
async def list_roles(service: PermissionService = Depends(get_permission_service)):
    return await service.list_roles()


@router.get(
    "/permissions",
    response_model=list[Permission],
    dependencies=[Depends(get_admin)],
)
async def list_permissions(service: PermissionService = Depends(get_permission_service)):
    return await service.list_permissions()


@router.post(
    "/assign-role",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_admin)],
)
async def assign_role(
    data: AssignRole, service: PermissionService = Depends(get_permission_service)
):
    await service.assign_role(data.user_id, data.role_id)
    return None
