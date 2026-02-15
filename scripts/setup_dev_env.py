#!/usr/bin/env python3
"""
KoreBase ERP - Master Setup Script
==================================
Automates the development environment setup for new contributors.
Works on Windows and Linux/macOS.

Usage:
    python scripts/setup_dev_env.py
"""

import os
import sys
import platform
import subprocess
import shutil
import secrets
from pathlib import Path

# --- Configuration ---
MIN_PYTHON_VERSION = (3, 10)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = PROJECT_ROOT / "venv"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"

def print_step(msg):
    print(f"\n✅ {msg}...")

def print_error(msg):
    print(f"\n❌ ERROR: {msg}")

def check_python_version():
    """Ensure Python version is compatible."""
    print_step("Checking Python version")
    current_version = sys.version_info
    if current_version < MIN_PYTHON_VERSION:
        print_error(f"Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ required. Found {current_version.major}.{current_version.minor}")
        sys.exit(1)
    print(f"   Python {current_version.major}.{current_version.minor} detected.")

def get_venv_python():
    """Return path to python executable inside venv."""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    else:
        return VENV_DIR / "bin" / "python"

def create_venv():
    """Create virtual environment if it doesn't exist."""
    if VENV_DIR.exists():
        print_step("Virtual environment already exists")
    else:
        print_step("Creating virtual environment")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
        except subprocess.CalledProcessError:
            print_error("Failed to create venv.")
            sys.exit(1)

def install_dependencies():
    """Install requirements using venv pip."""
    print_step("Installing dependencies")
    venv_python = get_venv_python()
    if not venv_python.exists():
        print_error(f"Venv python not found at {venv_python}")
        sys.exit(1)
        
    try:
        # Upgrade pip first
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
        # Install requirements
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)])
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies.")
        sys.exit(1)

def setup_env_file():
    """Create .env file from example if missing."""
    print_step("Configuring environment variables")
    if ENV_FILE.exists():
        print("   .env file already exists. Skipping creation.")
        return

    if not ENV_EXAMPLE.exists():
        print_error(".env.example not found! Cannot create .env")
        return

    print("   Creating .env from .env.example...")
    shutil.copy(ENV_EXAMPLE, ENV_FILE)
    
    # Read content
    content = ENV_FILE.read_text(encoding='utf-8')
    
    # Generate Secret Key
    secret_key = secrets.token_urlsafe(50)
    if 'your-secret-key-here' in content:
        content = content.replace('your-secret-key-here', secret_key)
        print("   Generated new secure SECRET_KEY.")
    
    # Interactive Setup?
    print("\n   [OPTIONAL CONFIGURATION]")
    email = input("   Enter DEFAULT_FROM_EMAIL (e.g. noreply@korebase.com) [Press Enter to skip]: ").strip()
    if email:
        # Simple string replacement for demonstration. A proper parser would be better but overkill here.
        # Assuming .env.example has a placeholder or we append
        if "DEFAULT_FROM_EMAIL=" in content:
             # This is a bit risky with replace if not exact, but sufficient for fresh .env
             pass # We'll just leave it for manual edit if complex
        else:
            content += f"\nDEFAULT_FROM_EMAIL={email}"

    # Write back
    ENV_FILE.write_text(content, encoding='utf-8')
    print("   .env created successfully.")

def run_migrations():
    """Run Django migrations."""
    print_step("Running database migrations")
    venv_python = get_venv_python()
    manage_py = PROJECT_ROOT / "manage.py"
    try:
        subprocess.check_call([str(venv_python), str(manage_py), "migrate"])
    except subprocess.CalledProcessError:
        print_error("Migration failed.")
        sys.exit(1)

def collect_static():
    """Collect static files."""
    print_step("Collecting static files")
    venv_python = get_venv_python()
    manage_py = PROJECT_ROOT / "manage.py"
    try:
        subprocess.check_call([str(venv_python), str(manage_py), "collectstatic", "--noinput"])
    except subprocess.CalledProcessError:
        print_error("Collectstatic failed.")

def check_superuser():
    """Prompt to create superuser."""
    print_step("Checking superuser")
    # We can check if any user exists via a simple script run
    venv_python = get_venv_python()
    manage_py = PROJECT_ROOT / "manage.py"
    check_script = "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())"
    
    try:
        # We need to set up django environment for this one-liner
        # Using shell command is cleaner
        cmd = [str(venv_python), str(manage_py), "shell", "-c", check_script]
        # Run command and decode output
        result = subprocess.check_output(cmd, text=True).strip()
        
        # Check if "True" is in the output (handling potential startup logs)
        if result and "True" in result.splitlines()[-1]: 
            print("   Superuser already exists.")
        else:
            print("\n   No superuser found.")
            create = input("   Do you want to create a superuser now? (y/n): ").lower().strip()
            if create == 'y':
                subprocess.check_call([str(venv_python), str(manage_py), "createsuperuser"])
    except subprocess.CalledProcessError:
        print("   Could not verify superuser status (database accessible?).")

def main():
    print("========================================")
    print("   KoreBase ERP - Dev Environment Setup")
    print("========================================")
    
    check_python_version()
    create_venv()
    install_dependencies()
    setup_env_file()
    run_migrations()
    collect_static()
    check_superuser()

    print("\n✅ SETUP COMPLETE!")
    print("========================================")
    
    if platform.system() == "Windows":
        activate_cmd = r".\venv\Scripts\activate"
    else:
        activate_cmd = "source venv/bin/activate"

    print(f"\nTo start development:")
    print(f"1. {activate_cmd}")
    print(f"2. python manage.py runserver")
    print("\nHappy Coding! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup aborted by user.")
        sys.exit(0)
