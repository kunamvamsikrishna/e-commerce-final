#!/usr/bin/env python3
"""
Environment setup script for Django Commerce App
This script helps you create a .env file with your API keys and secrets.
"""

import os
import secrets
from pathlib import Path

def generate_django_secret_key():
    """Generate a new Django secret key"""
    return secrets.token_urlsafe(50)

def create_env_file():
    """Create a .env file with template values"""
    env_path = Path('.env')
    
    if env_path.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Generate a new Django secret key
    django_secret_key = generate_django_secret_key()
    
    env_content = f"""# Django Settings
SECRET_KEY={django_secret_key}
DEBUG=True

# Stripe Configuration
STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key_here

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Google OAuth2
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_oauth2_key_here
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_oauth2_secret_here

# Database (if you want to use environment variables for database config)
DATABASE_URL=sqlite:///db.sqlite3
"""
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("\n📝 Next steps:")
    print("1. Edit the .env file and replace the placeholder values with your actual API keys")
    print("2. Never commit the .env file to version control")
    print("3. Keep your API keys secure")

if __name__ == "__main__":
    print("🔧 Django Commerce App Environment Setup")
    print("=" * 40)
    create_env_file() 