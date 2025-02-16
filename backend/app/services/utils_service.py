from pydantic.networks import EmailStr

from app.core.utils.email import generate_test_email, send_email
from app.models import Message


def send_test_email(email_to: EmailStr) -> Message:
    """Generate and send a test email."""
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")


def perform_health_check() -> bool:
    """Return API health status."""
    return True
