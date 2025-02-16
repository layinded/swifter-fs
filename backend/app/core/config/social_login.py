from pydantic import Field
from pydantic_settings import BaseSettings


class SocialLoginSettings(BaseSettings):
    ENABLE_SOCIAL_LOGIN: bool = Field(default=True)
    ENABLE_GOOGLE_LOGIN: bool = Field(default=True)
    ENABLE_FACEBOOK_LOGIN: bool = Field(default=False)
    ENABLE_GITHUB_LOGIN: bool = Field(default=False)

    # Google
    GOOGLE_AUTH_URL: str = Field(default=None)
    GOOGLE_CLIENT_ID: str = Field(default=None)
    GOOGLE_CLIENT_SECRET: str = Field(default=None)
    GOOGLE_REDIRECT_URI: str = Field(default=None)
    GOOGLE_SCOPE: str = Field(default=None)

    # Facebook
    FACEBOOK_AUTH_URL: str = Field(default=None)
    FACEBOOK_CLIENT_ID: str = Field(default=None)
    FACEBOOK_CLIENT_SECRET: str = Field(default=None)
    FACEBOOK_REDIRECT_URI: str = Field(default=None)
    FACEBOOK_SCOPE: str = Field(default=None)


social_login_settings = SocialLoginSettings()
