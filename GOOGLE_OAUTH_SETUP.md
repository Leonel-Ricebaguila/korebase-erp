# Google OAuth 2.0 Setup Guide

This guide walks you through setting up Google OAuth 2.0 authentication for the KoreBase ERP system.

## Overview

The Google OAuth implementation allows users to sign in using their Google accounts, providing a secure and convenient authentication method. The backend handles the OAuth flow, token exchange, user creation, and session management.

## Prerequisites

- Google Cloud Console account
- Access to the KoreBase ERP codebase
- Client secrets file from Google Cloud Console

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note down your Project ID

## Step 2: Enable Google+ API

1. In the Google Cloud Console, navigate to **APIs & Services** > **Library**
2. Search for "Google+ API" or "People API"
3. Enable the API for your project

## Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services** > **OAuth consent screen**
2. Choose **External** user type
3. Fill in the required information:
   - App name: "KoreBase ERP"
   - User support email: your email
   - Developer contact information: your email
4. Add the following scopes:
   - `openid`
   - `https://www.googleapis.com/auth/userinfo.email`
   - `https://www.googleapis.com/auth/userinfo.profile`
5. Save and publish the consent screen

## Step 4: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Select **Web application**
4. Configure the authorized redirect URIs:
   - Development: `http://localhost:8000/auth/google/callback/`
   - Production: `https://your-domain.com/auth/google/callback/`
5. Click **Create**
6. Download the JSON file containing your client secrets

## Step 5: Store Client Secrets Securely

### Option A: Store in Project Directory (Development)

1. Place the downloaded JSON file in your project root
2. Rename it to something like `client_secret.json`
3. Add it to `.gitignore` to prevent committing secrets

### Option B: Store in Secure Location (Production)

1. Store the JSON file in a secure directory outside your web root
2. Set appropriate file permissions (600 or 400)
3. Use environment variables to reference the path

## Step 6: Configure Environment Variables

Create or update your `.env` file:

```bash
# Google OAuth2.0 Configuration
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRETS_PATH=/path/to/your/client_secret.json
```

### Extracting Client ID from JSON

Open your client secrets JSON file and find the `client_id` field:

```json
{
  "web": {
    "client_id": "794121276402-lprvjjbhuh6pn2sc22hiqk1sn522edka.apps.googleusercontent.com",
    "client_secret": "your-secret-here",
    ...
  }
}
```

Copy the `client_id` value to your `.env` file.

## Step 7: Install Required Dependencies

The required libraries have been added to `requirements.txt`:

```bash
pip install google-auth-oauthlib google-api-python-client
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Step 8: Test the Implementation

### Development Testing

1. Start your Django development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to the login page: `http://localhost:8000/login/`

3. Click the "Sign in with Google" button

4. You should be redirected to Google's consent screen

5. After authorizing, you'll be redirected back and logged in

### Production Testing

1. Ensure your production environment variables are set
2. Verify the redirect URI matches your production domain
3. Test the flow in your production environment

## How It Works

### OAuth Flow

1. **Initiation**: User clicks "Sign in with Google"
2. **Redirect**: User is redirected to Google's OAuth consent screen
3. **Authorization**: User grants permissions to the application
4. **Callback**: Google redirects back with an authorization code
5. **Token Exchange**: Backend exchanges code for access token and ID token
6. **User Creation**: Backend creates or retrieves user account
7. **Session**: User is logged into Django

### Security Features

- **CSRF Protection**: State parameter prevents cross-site request forgery
- **Token Verification**: ID tokens are verified against Google's public keys
- **Secure Storage**: Client secrets stored via environment variables
- **HTTPS Required**: Production enforces secure connections
- **Email Verification**: Google accounts are automatically verified

### User Management

- **New Users**: Created automatically with Google account information
- **Existing Users**: Updated with latest Google profile data
- **Email Verified**: Google accounts are marked as verified
- **Username**: Generated from email prefix for compatibility

## Troubleshooting

### Common Issues

#### "redirect_uri_mismatch" Error

**Cause**: The redirect URI in Google Cloud Console doesn't match your application URL.

**Solution**: 
- Ensure the exact URL (including trailing slash) matches
- Check both development and production URIs
- Update the OAuth client ID configuration

#### "invalid_client" Error

**Cause**: Client ID or client secret is incorrect or missing.

**Solution**:
- Verify `GOOGLE_CLIENT_ID` in `.env` file
- Check that `GOOGLE_CLIENT_SECRETS_PATH` points to correct file
- Ensure the JSON file is valid and readable

#### "Error de seguridad: estado OAuth inválido"

**Cause**: CSRF protection detected a mismatch in state parameter.

**Solution**:
- Clear browser cookies and try again
- Check for session issues
- Ensure session middleware is properly configured

#### "Configuración de Google OAuth no encontrada"

**Cause**: Environment variables not set or file path incorrect.

**Solution**:
- Verify `.env` file exists and contains required variables
- Check that the client secrets file path is correct
- Ensure the application is loading environment variables

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
# In korebase/settings.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing Token Verification

You can test token verification manually:

```python
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

# Test token verification
id_info = id_token.verify_oauth2_token(
    token,
    google_requests.Request(),
    os.getenv('GOOGLE_CLIENT_ID')
)
print(id_info)
```

## Security Best Practices

1. **Never commit secrets**: Always add client secrets to `.gitignore`
2. **Use environment variables**: Store sensitive data in environment variables
3. **Rotate credentials**: Periodically update OAuth client secrets
4. **Monitor usage**: Check Google Cloud Console for suspicious activity
5. **Limit scopes**: Only request necessary permissions
6. **HTTPS only**: Always use HTTPS in production
7. **Regular audits**: Review OAuth configuration and access logs

## Frontend Integration

The frontend should provide a button that initiates the OAuth flow:

```html
<a href="{% url 'core:google_login' %}" class="btn-google">
    <img src="/static/images/google-logo.png" alt="Google">
    Sign in with Google
</a>
```

Or using JavaScript:

```javascript
function signInWithGoogle() {
    window.location.href = '/auth/google/';
}
```

## Production Deployment

### Render.com

1. Add environment variables in Render dashboard:
   - `GOOGLE_CLIENT_ID`: Your Google client ID
   - `GOOGLE_CLIENT_SECRETS_PATH`: Path to client secrets file (if stored)

2. Update authorized redirect URIs in Google Cloud Console:
   - Add your Render domain: `https://your-app.onrender.com/auth/google/callback/`

3. Deploy and test

### Other Platforms

Follow similar steps for other deployment platforms:
- Set environment variables
- Configure redirect URIs
- Ensure HTTPS is enabled
- Test the OAuth flow

## Maintenance

### Regular Tasks

- Monitor Google Cloud Console for usage statistics
- Review and update OAuth consent screen information
- Rotate client secrets periodically
- Check for deprecated APIs or scopes
- Update dependencies regularly

### Updating Client Secrets

If you need to regenerate client secrets:

1. Go to Google Cloud Console > Credentials
2. Delete existing OAuth client ID
3. Create new OAuth client ID
4. Download new client secrets file
5. Update environment variables
6. Update authorized redirect URIs
7. Test the new configuration

## Support

For issues or questions:

1. Check Google Cloud Console documentation
2. Review Django OAuth libraries documentation
3. Check application logs for detailed error messages
4. Verify environment variable configuration
5. Test with different Google accounts

## Additional Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Django Authentication Documentation](https://docs.djangoproject.com/en/stable/topics/auth/)
- [google-auth-oauthlib Documentation](https://google-auth-oauthlib.readthedocs.io/)

## Summary

The Google OAuth implementation provides a secure, user-friendly authentication method that integrates seamlessly with Django's authentication system. By following this guide, you can enable users to sign in with their Google accounts while maintaining security and data integrity.