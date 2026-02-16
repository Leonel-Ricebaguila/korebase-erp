# Google OAuth Quick Start - Using Provided Secrets

This guide helps you set up Google OAuth using the client secrets file you already have.

## Current Configuration

Your provided client secrets file contains:
- **Client ID**: `794121276402-lprvjjbhuh6pn2sc22hiqk1sn522edka.apps.googleusercontent.com`
- **Project ID**: `gen-lang-client-0660380898`
- **Current Redirect URI**: `http://127.0.0.1:8000/core/`

## ⚠️ Important: Redirect URI Mismatch

**Issue**: Your current Google OAuth configuration has the redirect URI set to `http://127.0.0.1:8000/core/`, but our Django implementation uses `/auth/google/callback/`.

**Solution**: You need to update the authorized redirect URIs in Google Cloud Console.

## Step-by-Step Setup

### 1. Update Google Cloud Console Redirect URIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: `gen-lang-client-0660380898`
3. Navigate to **APIs & Services** > **Credentials**
4. Find your OAuth 2.0 Client ID
5. Click the pencil icon to edit
6. **Remove** the old redirect URI: `http://127.0.0.1:8000/core/`
7. **Add** the new redirect URIs:
   - Development: `http://127.0.0.1:8000/auth/google/callback/`
   - Alternative: `http://localhost:8000/auth/google/callback/`
   - Production: `https://your-domain.com/auth/google/callback/`
8. Save the changes

### 2. Configure Environment Variables

Create or update your `.env` file with these values:

```bash
# Google OAuth2.0 Configuration
GOOGLE_CLIENT_ID=794121276402-lprvjjbhuh6pn2sc22hiqk1sn522edka.apps.googleusercontent.com
GOOGLE_CLIENT_SECRETS_PATH=/home/nico/Documents/DevSecOps/korebase-erp/client_secret_794121276402-lprvjjbhuh6pn2sc22hiqk1sn522edka.apps.googleusercontent.com.json
```

**Note**: Adjust the `GOOGLE_CLIENT_SECRETS_PATH` if you moved the file to a different location.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Configuration

Run the verification script:

```bash
python test_oauth_setup.py
```

This will check:
- ✅ Environment variables are set correctly
- ✅ Client secrets file exists and is valid
- ✅ Required dependencies are installed
- ✅ Django settings are configured
- ✅ OAuth views are implemented
- ✅ .gitignore is properly configured

### 5. Test the OAuth Flow

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/login/
   ```

3. Click the "Sign in with Google" button

4. You should be redirected to Google's consent screen

5. Authorize the application

6. You'll be redirected back and logged into your Django application

## Troubleshooting

### "redirect_uri_mismatch" Error

**Cause**: The redirect URI in Google Cloud Console doesn't match what your application is sending.

**Solution**:
1. Check the exact URL in the error message
2. Update Google Cloud Console with the correct redirect URI
3. Make sure to include the trailing slash: `/auth/google/callback/`

### "Configuración de Google OAuth no encontrada"

**Cause**: Environment variables not set correctly.

**Solution**:
1. Verify `.env` file exists in your project root
2. Check that `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRETS_PATH` are set
3. Ensure the path to the client secrets file is correct
4. Restart your Django server after changing environment variables

### Client Secrets File Not Found

**Cause**: The path to the client secrets file is incorrect.

**Solution**:
1. Check that the file exists at the specified path
2. Use absolute path or path relative to project root
3. Verify file permissions (should be readable by the application)

### OAuth Flow Not Working

**Steps to debug**:
1. Check Django logs for error messages
2. Verify environment variables are loaded: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GOOGLE_CLIENT_ID'))"`
3. Test the verification script: `python test_oauth_setup.py`
4. Check Google Cloud Console for any errors or warnings

## Production Deployment

When deploying to production:

1. **Update Redirect URIs** in Google Cloud Console:
   - Add your production domain: `https://your-domain.com/auth/google/callback/`

2. **Set Environment Variables** in your hosting platform:
   - `GOOGLE_CLIENT_ID`: Same as development
   - `GOOGLE_CLIENT_SECRETS_PATH`: Path to client secrets file on the server

3. **Security Considerations**:
   - Store client secrets file outside web root
   - Set proper file permissions (600 or 400)
   - Use HTTPS in production
   - Never commit secrets to version control

## File Locations

Your current setup:
- **Client Secrets**: `client_secret_794121276402-lprvjjbhuh6pn2sc22hiqk1sn522edka.apps.googleusercontent.com.json`
- **Environment File**: `.env` (create this in project root)
- **OAuth Views**: `core/views.py` (google_login_view, google_callback_view)
- **URL Configuration**: `core/urls.py` (/auth/google/, /auth/google/callback/)

## Quick Reference

### Environment Variables
```bash
GOOGLE_CLIENT_ID=794121276402-lprvjjbhuh6pn2sc22hiqk1sn522edka.apps.googleusercontent.com
GOOGLE_CLIENT_SECRETS_PATH=/path/to/client_secret_794121276402-lprvjjbhuh6pn2sc22hiqk1sn522edka.apps.googleusercontent.com.json
```

### OAuth Endpoints
- **Login Initiation**: `/auth/google/`
- **Callback Handler**: `/auth/google/callback/`

### Required Redirect URIs
- Development: `http://127.0.0.1:8000/auth/google/callback/`
- Production: `https://your-domain.com/auth/google/callback/`

## Next Steps

1. ✅ Update Google Cloud Console redirect URIs
2. ✅ Configure environment variables in `.env`
3. ✅ Install dependencies
4. ✅ Run verification script
5. ✅ Test OAuth flow
6. ✅ Deploy to production

For detailed information, see [`GOOGLE_OAUTH_SETUP.md`](GOOGLE_OAUTH_SETUP.md).

## Support

If you encounter issues:
1. Run `python test_oauth_setup.py` to diagnose problems
2. Check Django logs for detailed error messages
3. Verify Google Cloud Console configuration
4. Ensure all environment variables are set correctly

The implementation is ready to use once you update the redirect URIs in Google Cloud Console and configure your environment variables!