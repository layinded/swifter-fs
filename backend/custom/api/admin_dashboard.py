from fastapi import APIRouter, Depends

from app.core.security.dependencies import require_roles

router = APIRouter()


@router.get(
    "/admin/dashboard", dependencies=[Depends(require_roles("admin", "is_superuser"))]
)
def get_admin_dashboard():
    return {"message": "Welcome to the admin dashboard"}
