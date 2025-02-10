from datetime import timedelta

from app.core.config.settings import settings
from app.core.config.social_login import social_login_settings
from app.core.security import refresh_token_service
from app.core.security.dependencies import SessionDep
from app.crud import crud_user
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, HTTPException, Request
import requests

router = APIRouter()
oauth = OAuth()

# ✅ Register Google OAuth
if social_login_settings.ENABLE_GOOGLE_LOGIN:
    oauth.register(
        name="google",
        client_id=social_login_settings.GOOGLE_CLIENT_ID,
        client_secret=social_login_settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
if social_login_settings.ENABLE_FACEBOOK_LOGIN:
    oauth.register(
        name="facebook",
        client_id=social_login_settings.FACEBOOK_CLIENT_ID,
        client_secret=social_login_settings.FACEBOOK_CLIENT_SECRET,
        access_token_url="https://graph.facebook.com/v12.0/oauth/access_token",
        authorize_url="https://www.facebook.com/v12.0/dialog/oauth",
        client_kwargs={"scope": "email,public_profile"},
    )


@router.get("/google/auth")
async def google_login(request: Request):
    """
    Redirect the user to Google OAuth for authentication.
    """
    try:
        # 🔍 Ensure Google OAuth is enabled
        if not social_login_settings.ENABLE_GOOGLE_LOGIN:
            raise HTTPException(status_code=400, detail="Google login is disabled.")

        # ✅ Ensure the redirect URI is configured correctly
        redirect_uri = social_login_settings.GOOGLE_REDIRECT_URI
        if not redirect_uri:
            raise HTTPException(status_code=500, detail="Google OAuth redirect URI is not configured.")

        # ✅ Debugging session before redirect
        print(f"🔍 Before Redirect - Session: {request.session}")

        return await oauth.google.authorize_redirect(request, redirect_uri)

    except Exception as e:
        print(f"❌ Google Login Error: {str(e)}")  # Debugging
        raise HTTPException(status_code=500, detail=f"Failed to initiate Google login: {str(e)}")


@router.get("/google/auth/callback")
async def google_auth_callback(request: Request, session: SessionDep):
    """
    Handle Google OAuth callback and return a JWT token.
    """
    try:
        # 🔍 Check if `state` and `code` exist in the request
        state = request.query_params.get("state")
        code = request.query_params.get("code")

        if not state:
            return {"error": "Missing state parameter. Please use the correct Google OAuth login URL."}

        if not code:
            return {"error": "Missing authorization code. Please try logging in again."}

        # ✅ Debugging session state
        print(f"🔍 Session before callback: {request.session}")

        # 🔑 Exchange the authorization code for a token
        token = await oauth.google.authorize_access_token(request)

        if not token:
            raise HTTPException(status_code=400, detail="Failed to fetch token from Google.")

        user_info = token.get("userinfo", {})
        email = user_info.get("email")

        if not email:
            raise HTTPException(status_code=400, detail="Google account missing email.")

        # 🔍 Check if user exists, otherwise create a new social login user
        existing_user = crud_user.get_user_by_email(session=session, email=email)

        if not existing_user:
            existing_user = crud_user.create_social_user(session, email, user_info, "google")

        # ✅ Always generate access and refresh tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = refresh_token_service.create_access_token(existing_user.email,
                                                                 expires_delta=access_token_expires)
        refresh_token = refresh_token_service.create_refresh_token(session, existing_user.email,
                                                                   expires_delta=refresh_token_expires)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,  # ✅ Always send refresh token
            "token_type": "bearer",
        }

    except Exception as e:
        print(f"❌ Google OAuth Callback Error: {str(e)}")  # Debugging
        return {"error": f"Authentication failed: {str(e)}"}


@router.get("/facebook/auth")
async def facebook_login(request: Request):
    """
    Redirect the user to Facebook OAuth for authentication.
    """
    try:
        if not social_login_settings.ENABLE_FACEBOOK_LOGIN:
            raise HTTPException(status_code=400, detail="Facebook login is disabled.")

        redirect_uri = social_login_settings.FACEBOOK_REDIRECT_URI
        if not redirect_uri:
            raise HTTPException(status_code=500, detail="Facebook OAuth redirect URI is not configured.")

        # ✅ Debugging before redirect
        print(f"🔍 Before Redirect - Session: {request.session}")

        return await oauth.facebook.authorize_redirect(request, redirect_uri)

    except Exception as e:
        print(f"❌ Facebook Login Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate Facebook login: {str(e)}")


async def fetch_facebook_user_info(access_token: str):
    """
    Fetch user details from Facebook Graph API
    """
    user_info_url = "https://graph.facebook.com/me?fields=id,name,email"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(user_info_url, headers=headers)
    user_data = response.json()

    if "error" in user_data:
        raise HTTPException(status_code=400, detail=f"Facebook API Error: {user_data['error']['message']}")

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
            raise HTTPException(status_code=400, detail="Invalid OAuth response. Missing required parameters.")

        print(f"🔍 Session before callback: {request.session}")

        # 🔑 Exchange code for access token
        token = await oauth.facebook.authorize_access_token(request)
        if not token:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token from Facebook.")

        access_token = token.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Facebook did not return an access token.")

        # ✅ Corrected: Await the async function
        user_info = await fetch_facebook_user_info(access_token)
        email = user_info.get("email")

        if not email:
            raise HTTPException(status_code=400,
                                detail="Facebook account missing email. Please ensure your Facebook account has a public email.")

        # 🔍 Check if user exists, otherwise create new social login user
        existing_user = crud_user.get_user_by_email(session=session, email=email)

        if not existing_user:
            existing_user = crud_user.create_social_user(session, email, user_info, "facebook")

        # ✅ Always generate access and refresh tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = refresh_token_service.create_access_token(existing_user.email,
                                                                 expires_delta=access_token_expires)
        refresh_token = refresh_token_service.create_refresh_token(session, existing_user.email,
                                                                   expires_delta=refresh_token_expires)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    except Exception as e:
        print(f"❌ Facebook OAuth Callback Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")
