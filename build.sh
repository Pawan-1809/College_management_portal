#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Render deployment build process..."

echo "🔍 Checking Python version..."
python --version
PYTHON_VER=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Detected Python version: $PYTHON_VER"
if [[ "$PYTHON_VER" != "3.9" ]]; then
    echo "❌ Error: Expected Python 3.9, but got Python $PYTHON_VER"
    echo "Please check PYTHON_VERSION environment variable and .python-version file"
    exit 1
fi
echo "✅ Python 3.9 confirmed"

echo "🔧 Upgrading pip..."
pip install --upgrade pip

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

echo "🔍 Verifying PostgreSQL adapter..."
python -c "import psycopg2; print('✅ psycopg2 installed successfully')"

echo "📦 Collecting static files safely..."
# Use our custom safe_collectstatic command that handles missing files
echo "Note: Using safe collection method for missing jQuery UI files"
python manage.py safe_collectstatic --no-input || {
    echo "⚠️  Safe collectstatic failed, trying standard method..."
    python manage.py collectstatic --no-input || {
        echo "⚠️  Standard collectstatic failed, trying without clearing..."
        python manage.py collectstatic --no-input
    }
}

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
