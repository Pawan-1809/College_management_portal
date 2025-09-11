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

echo "🔧 Fixing jQuery UI CSS file paths..."
python fix_jquery_ui.py

echo "📦 Collecting static files..."
# Use basic Django static files storage (no manifest processing)
echo "Using basic static files storage - jQuery UI paths have been fixed"
python manage.py collectstatic --no-input --clear

echo "🔄 Running database migrations..."
python manage.py migrate

echo "👤 Creating default superuser if needed..."
python manage.py create_default_superuser || {
    echo "⚠️  Custom command failed, trying alternative..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@college.edu', 'admin123', first_name='Admin', last_name='User') if not User.objects.filter(is_superuser=True).exists() else print('Superuser exists')" | python manage.py shell
}

echo "✅ Build completed successfully!"
