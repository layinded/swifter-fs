from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config.settings import settings
from app.core.security.dependencies import CurrentUser, SessionDep
from app.core.security.password_security import (
    generate_password_reset_token,
    get_password_hash,
    verify_password_reset_token,
)
from app.core.security.refresh_token_service import (
    create_access_token,
    create_refresh_token,
    revoke_all_tokens,
    revoke_refresh_token,
    verify_refresh_token,
)
from app.core.utils.email import generate_reset_password_email, send_email
from app.core.utils.translation_helper import translate
from app.crud import crud_user
from app.models import common, user
from app.models.auth import Token, TokenRefreshRequest
from app.services import user_service

router = APIRouter()


@router.post("/login", response_model=Token)
def login_user(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
) -> Token:
    """OAuth2 login that returns an access token and refresh token."""
    existing_user = crud_user.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not existing_user:
        raise HTTPException(
            status_code=400, detail=translate(request, "incorrect_email_or_password")
        )
    if not existing_user.is_active:
        raise HTTPException(status_code=400, detail=translate(request, "inactive_user"))

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        existing_user.email, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        session, existing_user.email, expires_delta=refresh_token_expires
    )

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/token/refresh", response_model=Token)
def refresh_access_token(
    session: SessionDep, request_data: TokenRefreshRequest, request: Request
) -> Token:
    """Verify refresh token and issue a new access token with a new refresh token."""
    result = verify_refresh_token(session, request_data.refresh_token, request)
    if not result:
        raise HTTPException(
            status_code=401,
            detail=translate(request, "invalid_or_expired_refresh_token"),
        )

    email, auth_provider = result
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    new_access_token = create_access_token(
        email, expires_delta=access_token_expires, auth_provider=auth_provider
    )
    new_refresh_token = create_refresh_token(
        session, email, expires_delta=refresh_token_expires, auth_provider=auth_provider
    )

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


@router.post(
    "/register", response_model=user.UserPublic, operation_id="register_new_user"
)
def register_user(
    session: SessionDep, user_in: user.UserRegister, request: Request
) -> Any:
    """Public endpoint to register a new user."""
    try:
        return user_service.register_user(session, user_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail=translate(request, "user_already_exists")
        )


@router.get("/profile", response_model=user.UserPublic, operation_id="get_current_user")
def read_user_me(current_user: CurrentUser) -> Any:
    """Get details of the currently logged-in user."""
    return current_user


@router.patch(
    "/password/update", response_model=common.Message, operation_id="change_password"
)
def update_password(
    session: SessionDep,
    body: user.UpdatePassword,
    current_user: CurrentUser,
    request: Request,
) -> Any:
    """Update the password for the currently logged-in user."""
    # The service returns a message or you can create your own
    user_service.update_password(
        session, current_user.id, body.current_password, body.new_password
    )
    return common.Message(message=translate(request, "password_updated_successfully"))


@router.delete(
    "/profile/delete", response_model=common.Message, operation_id="delete_current_user"
)
def delete_user_me(
    session: SessionDep, current_user: CurrentUser, request: Request = None
) -> Any:
    """Delete the currently logged-in user account."""
    user_service.delete_self(session, current_user)
    return common.Message(message=translate(request, "user_deleted_successfully"))


@router.post("/token/revoke")
def logout(session: SessionDep, request_data: TokenRefreshRequest, request: Request):
    """Revoke the provided refresh token to log the user out."""
    result = verify_refresh_token(session, request_data.refresh_token, request)
    if not result:
        raise HTTPException(
            status_code=401,
            detail=translate(request, "invalid_or_expired_refresh_token"),
        )
    revoked = revoke_refresh_token(session, request_data.refresh_token)
    if not revoked:
        raise HTTPException(
            status_code=401, detail=translate(request, "token_already_revoked")
        )
    return {"message": translate(request, "logged_out_successfully")}


@router.post("/password/recover/{email}", response_model=common.Message)
def recover_password(
    email: str, session: SessionDep, request: Request = None
) -> common.Message:
    """Send password recovery email if the user exists."""
    existing_user = crud_user.get_user_by_email(session=session, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=translate(request, "user_email_not_found")
        )
    if existing_user.auth_provider != "local":
        raise HTTPException(
            status_code=400, detail=translate(request, "password_reset_not_available")
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=existing_user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=existing_user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return common.Message(
        message=translate(request, "password_recovery_email_sent_successfully")
    )


@router.post("/password/reset", response_model=common.Message)
def reset_password(
    session: SessionDep, body: user.NewPassword, request: Request = None
) -> common.Message:
    """Reset password using a valid token."""
    email = verify_password_reset_token(body.token)
    if not email:
        raise HTTPException(
            status_code=400, detail=translate(request, "invalid_or_expired_reset_token")
        )
    existing_user = crud_user.get_user_by_email(session=session, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=translate(request, "user_not_found")
        )
    if existing_user.auth_provider != "local":
        raise HTTPException(
            status_code=400, detail=translate(request, "password_reset_not_available")
        )
    existing_user.hashed_password = get_password_hash(body.new_password)
    session.add(existing_user)
    session.commit()
    revoke_all_tokens(session, email)  # Force logout after password reset
    return common.Message(message=translate(request, "password_reset_successful"))
