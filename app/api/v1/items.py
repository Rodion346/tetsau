from fastapi import APIRouter, Depends, HTTPException, status

from app.api.depence import get_user, get_permission_service
from app.schemas.user import User
from app.services.permission import PermissionService

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
async def list_items(
    user: User = Depends(get_user),
    permission_service: PermissionService = Depends(get_permission_service),
):
    if not await permission_service.user_has_permission(user.id, "items:read"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return [
        {"id": 1, "name": "Sample"},
    ]


@router.post("/")
async def create_item(
    user: User = Depends(get_user),
    permission_service: PermissionService = Depends(get_permission_service),
):
    if not await permission_service.user_has_permission(user.id, "items:create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return {"status": "created"}
