### Social Login Configuration

Swifter-FS supports social login with Google, Facebook, and GitHub. You can enable or disable social login and specific providers by updating the `.env` file.

#### Enable Social Login
Set `ENABLE_SOCIAL_LOGIN` to `true` or `false`.

#### Enable Specific Providers
- `ENABLE_GOOGLE_LOGIN`: Enable or disable Google login.
- `ENABLE_FACEBOOK_LOGIN`: Enable or disable Facebook login.
- `ENABLE_GITHUB_LOGIN`: Enable or disable GitHub login.

#### Example `.env`
```env
ENABLE_SOCIAL_LOGIN=true
ENABLE_GOOGLE_LOGIN=true
ENABLE_FACEBOOK_LOGIN=false
ENABLE_GITHUB_LOGIN=false

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
