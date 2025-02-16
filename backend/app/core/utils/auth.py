# Authentication logic
from datetime import timedelta
from starlette.responses import JSONResponse, RedirectResponse
from fastapi import Request
from app.core.config.settings import settings
from app.core.security import refresh_token_service
from sqlalchemy.orm import Session


def generate_tokens_and_respond(request: Request, session: Session, user_email: str):
    """
    Generates access and refresh tokens, and returns either JSON or redirects the user.

    :param request: The FastAPI request object
    :param session: The database session
    :param user_email: The email of the authenticated user
    :return: JSONResponse for API clients or RedirectResponse for web users
    """
    front_url = settings.FRONTEND_HOST  # Fetch from backend .env

    # ✅ Generate access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = refresh_token_service.create_access_token(
        user_email, expires_delta=access_token_expires
    )
    refresh_token = refresh_token_service.create_refresh_token(
        session, user_email, expires_delta=refresh_token_expires
    )

    # 🔹 Check if the request comes from an API client (e.g., Mobile)
    accept_header = request.headers.get("accept", "")
    if "application/json" in accept_header:
        return JSONResponse({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        })

    # ✅ Redirect web users to frontend
    return RedirectResponse(
        url=f"{front_url}/oauth-success?access_token={access_token}&refresh_token={refresh_token}"
    )
