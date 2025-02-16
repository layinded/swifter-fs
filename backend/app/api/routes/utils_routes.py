from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.core.security.dependencies import get_current_active_superuser
from app.models import Message
from app.services import utils_service

router = APIRouter()


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Send a test email (Admin Only).
    """
    return utils_service.send_test_email(email_to)


@router.get("/health-check/")
async def health_check() -> bool:
    """
    Check if the API is running.
    """
    return utils_service.perform_health_check()
