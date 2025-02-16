from fastapi import APIRouter, Depends

from app.core.security.dependencies import get_current_user

router = APIRouter()


@router.get("/reports/stats")
def get_stats(user=Depends(get_current_user)):
    return {"message": "This is a protected report", "user": user.email}
