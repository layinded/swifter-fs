from unittest.mock import MagicMock, patch

from app.api.email_utils import perform_health_check, send_test_email
from app.models import Message


def test_perform_health_check():
    # Verify that the health check returns True
    assert perform_health_check() is True


@patch("app.api.email_utils.send_email")
@patch("app.api.email_utils.generate_test_email")
def test_send_test_email(mock_generate_test_email, mock_send_email):
    # Create a dummy email_data object with the expected attributes.
    dummy_email_data = MagicMock()
    dummy_email_data.subject = "Test Subject"
    dummy_email_data.html_content = "<p>Test Content</p>"
    mock_generate_test_email.return_value = dummy_email_data

    email_to = "test@example.com"
    result = send_test_email(email_to)

    # Verify that generate_test_email was called correctly.
    mock_generate_test_email.assert_called_once_with(email_to=email_to)

    # Verify that send_email was called with the correct arguments.
    mock_send_email.assert_called_once_with(
        email_to=email_to,
        subject=dummy_email_data.subject,
        html_content=dummy_email_data.html_content,
    )

    # Check that the returned Message is as expected.
    assert isinstance(result, Message)
    assert result.message == "Test email sent"
