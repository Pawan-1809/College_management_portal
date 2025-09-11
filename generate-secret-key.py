#!/usr/bin/env python
"""
Generate a secure Django SECRET_KEY for deployment
"""
import secrets
import string

def generate_secret_key():
    """Generate a secure random secret key"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(50))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("=" * 60)
    print("🔐 Django SECRET_KEY Generated")
    print("=" * 60)
    print(f"SECRET_KEY={secret_key}")
    print("=" * 60)
    print("💡 Copy this to your .env file or environment variables")
    print("⚠️  Keep this secret and never commit it to version control!")
    print("=" * 60)
