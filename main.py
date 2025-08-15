from fastapi import FastAPI

from app.api.v1.auth.auth import router as auth_router
from app.api.v1.admin.roles import router as admin_router
from app.api.v1.items import router as items_router
from app.api.depence import get_permission_service
from app.core.db_helper import db_helper
from app.core.models import User
from app.services.permission import PermissionService
from sqladmin import Admin, ModelView


app = FastAPI()

admin = Admin(app, db_helper.engine)


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        User.first_name,
        User.last_name,
    ]


admin.add_view(UserAdmin)


@app.on_event("startup")
async def startup() -> None:
    service: PermissionService = await get_permission_service()
    await service.ensure_defaults()


app.include_router(auth_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(items_router, prefix="/api/v1")
