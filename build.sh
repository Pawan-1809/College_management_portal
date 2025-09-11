#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Render deployment build process..."

echo "🔧 Upgrading pip..."
pip install --upgrade pip

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

echo "🔍 Verifying PostgreSQL adapter..."
python -c "import psycopg2; print('✅ psycopg2 installed successfully')"

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "🔄 Running database migrations..."
python manage.py migrate

echo "👤 Creating default superuser if needed..."
python -c "
from django.contrib.auth import get_user_model
from django.db import IntegrityError
User = get_user_model()
try:
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            email='admin@college.edu',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print('✅ Default superuser created successfully!')
    else:
        print('ℹ️  Superuser already exists')
except Exception as e:
    print(f'⚠️  Could not create superuser: {e}')
"

echo "✅ Build completed successfully!"
