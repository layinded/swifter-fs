import secrets

import requests
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import JSONResponse

from app.core.config.settings import settings
from app.core.config.social_login import social_login_settings
from app.core.security.dependencies import SessionDep
from app.core.utils.auth import generate_tokens_and_respond
from app.core.utils.translation_helper import translate
from app.crud import crud_user

router = APIRouter()
oauth = OAuth()

# Register Google OAuth
if social_login_settings.ENABLE_GOOGLE_LOGIN:
    oauth.register(
        name="google",
        client_id=social_login_settings.GOOGLE_CLIENT_ID,
        client_secret=social_login_settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

# Register Facebook OAuth
if social_login_settings.ENABLE_FACEBOOK_LOGIN:
    oauth.register(
        name="facebook",
        client_id=social_login_settings.FACEBOOK_CLIENT_ID,
        client_secret=social_login_settings.FACEBOOK_CLIENT_SECRET,
        access_token_url="https://graph.facebook.com/v12.0/oauth/access_token",
        authorize_url="https://www.facebook.com/v12.0/dialog/oauth",
        client_kwargs={"scope": "email,public_profile"},
    )


@router.get("/urls")
def get_oauth_urls():
    """
    Return OAuth login URLs dynamically from environment variables.
    """
    base_url = settings.BACKEND_HOST
    urls = {
        "google": f"{base_url}/api/v1/oauth/google/auth"
        if social_login_settings.ENABLE_SOCIAL_LOGIN
        and social_login_settings.ENABLE_GOOGLE_LOGIN
        else None,
        "facebook": f"{base_url}/api/v1/oauth/facebook/auth"
        if social_login_settings.ENABLE_SOCIAL_LOGIN
        and social_login_settings.ENABLE_FACEBOOK_LOGIN
        else None,
    }
    return JSONResponse(urls)


@router.get("/google/auth")
async def google_login(request: Request):
    """
    Redirect the user to Google OAuth for authentication.
    """
    try:
        if not social_login_settings.ENABLE_GOOGLE_LOGIN:
            raise HTTPException(
                status_code=400, detail=translate(request, "google_login_disabled")
            )
        redirect_uri = social_login_settings.GOOGLE_REDIRECT_URI
        if not redirect_uri:
            raise HTTPException(
                status_code=500,
                detail=translate(request, "google_redirect_uri_not_configured"),
            )
        state = secrets.token_urlsafe(16)
        request.session["oauth_state"] = state
        return await oauth.google.authorize_redirect(request, redirect_uri, state=state)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=translate(request, "failed_to_initiate_google_login", error=str(e)),
        )


@router.get("/google/auth/callback")
async def google_auth_callback(request: Request, session: SessionDep):
    """
    Handle Google OAuth callback and return a JWT token for API clients or redirect web users.
    """
    try:
        state = request.query_params.get("state")
        stored_state = request.session.get("oauth_state")
        if not stored_state or state != stored_state:
            return JSONResponse(
                {"error": translate(request, "csrf_warning_state_mismatch")},
                status_code=400,
            )
        token = await oauth.google.authorize_access_token(request)
        if not token:
            return JSONResponse(
                {"error": translate(request, "failed_to_fetch_google_token")},
                status_code=400,
            )
        user_info = token.get("userinfo", {})
        email = user_info.get("email")
        if not email:
            return JSONResponse(
                {"error": translate(request, "google_account_missing_email")},
                status_code=400,
            )
        existing_user = crud_user.get_user_by_email(session=session, email=email)
        if not existing_user:
            existing_user = crud_user.create_social_user(
                session, email, user_info, "google"
            )
        request.session.pop("oauth_state", None)
        return generate_tokens_and_respond(request, session, existing_user.email)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=translate(request, "google_auth_callback_failed", error=str(e)),
        )


@router.get("/facebook/auth")
async def facebook_login(request: Request):
    """
    Redirect the user to Facebook OAuth for authentication.
    """
    try:
        if not social_login_settings.ENABLE_FACEBOOK_LOGIN:
            raise HTTPException(
                status_code=400, detail=translate(request, "facebook_login_disabled")
            )
        redirect_uri = social_login_settings.FACEBOOK_REDIRECT_URI
        if not redirect_uri:
            raise HTTPException(
                status_code=500,
                detail=translate(request, "facebook_redirect_uri_not_configured"),
            )
        return await oauth.facebook.authorize_redirect(request, redirect_uri)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=translate(
                request, "failed_to_initiate_facebook_login", error=str(e)
            ),
        )


async def fetch_facebook_user_info(access_token: str):
    """
    Fetch user details from Facebook Graph API.
    """
    user_info_url = "https://graph.facebook.com/me?fields=id,name,email"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(user_info_url, headers=headers)
    user_data = response.json()
    if "error" in user_data:
        raise HTTPException(
            status_code=400,
            detail=f"Facebook API Error: {user_data['error']['message']}",
        )
    return user_data


@router.get("/facebook/auth/callback")
async def facebook_auth_callback(request: Request, session: SessionDep):
    """
    Handle Facebook OAuth callback and return a JWT token.
    """
    try:
        state = request.query_params.get("state")
        code = request.query_params.get("code")
        if not state or not code:
            raise HTTPException(
                status_code=400, detail=translate(request, "invalid_oauth_response")
            )
        token = await oauth.facebook.authorize_access_token(request)
        if not token:
            raise HTTPException(
                status_code=400,
                detail=translate(request, "failed_to_retrieve_facebook_token"),
            )
        access_token = token.get("access_token")
        if not access_token:
            raise HTTPException(
                status_code=400,
                detail=translate(request, "facebook_missing_access_token"),
            )
        user_info = await fetch_facebook_user_info(access_token)
        email = user_info.get("email")
        if not email:
            raise HTTPException(
                status_code=400,
                detail=translate(request, "facebook_account_missing_email"),
            )
        existing_user = crud_user.get_user_by_email(session=session, email=email)
        if not existing_user:
            existing_user = crud_user.create_social_user(
                session, email, user_info, "facebook"
            )
        return generate_tokens_and_respond(request, session, existing_user.email)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=translate(request, "facebook_auth_callback_failed", error=str(e)),
        )
