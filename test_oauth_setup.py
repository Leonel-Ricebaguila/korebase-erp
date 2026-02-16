#!/usr/bin/env python
"""
Google OAuth Setup Verification Script
Tests that all components are properly configured for Google OAuth
"""
import os
import sys
import json
from pathlib import Path

def check_environment_variables():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = [
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRETS_PATH'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"  ❌ {var} is not set")
        else:
            print(f"  ✅ {var} is set")
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All required environment variables are set")
    return True


def check_client_secrets_file():
    """Check if client secrets file exists and is valid"""
    print("\n🔍 Checking client secrets file...")
    
    secrets_path = os.getenv('GOOGLE_CLIENT_SECRETS_PATH')
    if not secrets_path:
        print("  ❌ GOOGLE_CLIENT_SECRETS_PATH not set")
        return False
    
    secrets_file = Path(secrets_path)
    if not secrets_file.exists():
        print(f"  ❌ Client secrets file not found at: {secrets_path}")
        return False
    
    print(f"  ✅ Client secrets file found at: {secrets_path}")
    
    # Check if file is readable
    try:
        with open(secrets_file, 'r') as f:
            secrets_data = json.load(f)
        
        # Check required fields
        required_fields = ['web']
        for field in required_fields:
            if field not in secrets_data:
                print(f"  ❌ Missing required field in client secrets: {field}")
                return False
        
        web_data = secrets_data['web']
        if 'client_id' not in web_data:
            print("  ❌ Missing client_id in client secrets")
            return False
        
        print("  ✅ Client secrets file is valid JSON")
        print(f"  ✅ Client ID: {web_data['client_id']}")
        
        # Verify client ID matches environment variable
        env_client_id = os.getenv('GOOGLE_CLIENT_ID')
        if env_client_id != web_data['client_id']:
            print(f"  ⚠️  Client ID mismatch between env var and secrets file")
            print(f"     Env var: {env_client_id}")
            print(f"     Secrets file: {web_data['client_id']}")
        
        return True
        
    except json.JSONDecodeError:
        print("  ❌ Client secrets file is not valid JSON")
        return False
    except Exception as e:
        print(f"  ❌ Error reading client secrets file: {str(e)}")
        return False


def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n🔍 Checking required dependencies...")
    
    required_packages = [
        'google_auth_oauthlib',
        'googleapiclient',
        'google.oauth2',
        'google.auth'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package} is not installed")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies are installed")
    return True


def check_django_settings():
    """Check if Django settings are properly configured"""
    print("\n🔍 Checking Django settings...")
    
    try:
        # Add project root to Python path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        # Import Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korebase.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        # Check if OAuth settings exist
        if hasattr(settings, 'GOOGLE_CLIENT_ID'):
            print(f"  ✅ GOOGLE_CLIENT_ID in settings")
        else:
            print("  ❌ GOOGLE_CLIENT_ID not in settings")
            return False
        
        if hasattr(settings, 'GOOGLE_CLIENT_SECRETS_PATH'):
            print(f"  ✅ GOOGLE_CLIENT_SECRETS_PATH in settings")
        else:
            print("  ❌ GOOGLE_CLIENT_SECRETS_PATH not in settings")
            return False
        
        # Check if URLs are configured
        try:
            from django.urls import reverse
            try:
                reverse('core:google_login')
                print("  ✅ Google login URL is configured")
            except:
                print("  ❌ Google login URL is not configured")
                return False
            
            try:
                reverse('core:google_callback')
                print("  ✅ Google callback URL is configured")
            except:
                print("  ❌ Google callback URL is not configured")
                return False
                
        except Exception as e:
            print(f"  ❌ Error checking URL configuration: {str(e)}")
            return False
        
        print("✅ Django settings are properly configured")
        return True
        
    except Exception as e:
        print(f"  ❌ Error loading Django settings: {str(e)}")
        return False


def check_views():
    """Check if OAuth views are implemented"""
    print("\n🔍 Checking OAuth views...")
    
    try:
        from core.views import google_login_view, google_callback_view
        print("  ✅ google_login_view function exists")
        print("  ✅ google_callback_view function exists")
        print("✅ OAuth views are properly implemented")
        return True
    except ImportError as e:
        print(f"  ❌ Error importing OAuth views: {str(e)}")
        return False


def check_gitignore():
    """Check if client secrets are properly ignored"""
    print("\n🔍 Checking .gitignore configuration...")
    
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        print("  ⚠️  .gitignore file not found")
        return True  # Not critical
    
    with open(gitignore_path, 'r') as f:
        gitignore_content = f.read()
    
    required_patterns = [
        'client_secret*.json',
        '*client_secret*.json',
        '.env'
    ]
    
    missing_patterns = []
    for pattern in required_patterns:
        if pattern not in gitignore_content:
            missing_patterns.append(pattern)
            print(f"  ⚠️  Pattern not in .gitignore: {pattern}")
        else:
            print(f"  ✅ Pattern in .gitignore: {pattern}")
    
    if missing_patterns:
        print(f"\n⚠️  Consider adding these patterns to .gitignore")
    else:
        print("✅ .gitignore properly configured")
    
    return True


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("🔐 Google OAuth Setup Verification")
    print("=" * 60)
    
    # Load environment variables from .env file if it exists
    env_file = Path('.env')
    if env_file.exists():
        print(f"\n📝 Loading environment variables from .env file...")
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            print("  ⚠️  python-dotenv not installed, skipping .env file loading")
    
    # Run all checks
    checks = [
        check_environment_variables,
        check_client_secrets_file,
        check_dependencies,
        check_django_settings,
        check_views,
        check_gitignore
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Error running check: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Verification Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if all(results):
        print("\n✅ All checks passed! Your Google OAuth setup is ready.")
        print("\n🚀 Next steps:")
        print("1. Start your Django development server")
        print("2. Navigate to the login page")
        print("3. Click 'Sign in with Google'")
        print("4. Test the OAuth flow")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\n📖 For detailed setup instructions, see GOOGLE_OAUTH_SETUP.md")
        return 1


if __name__ == '__main__':
    sys.exit(main())