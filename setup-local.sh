#!/bin/bash
# Local Development Setup Script for College Management Portal

echo "🛠️ Setting up College Management Portal for local development..."

# Check Python version
echo "🐍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | grep -Po '(?<=Python )(.+)')
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    
    # Generate a random secret key
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    
    # Update .env file with development settings
    sed -i "s/your-secret-key-here/$SECRET_KEY/" .env
    sed -i "s/DEBUG=False/DEBUG=True/" .env
    sed -i "s/DB_ENGINE=django.db.backends.postgresql/DB_ENGINE=django.db.backends.sqlite3/" .env
    sed -i "s/SECURE_SSL_REDIRECT=True/SECURE_SSL_REDIRECT=False/" .env
    sed -i "s/SESSION_COOKIE_SECURE=True/SESSION_COOKIE_SECURE=False/" .env
    sed -i "s/CSRF_COOKIE_SECURE=True/CSRF_COOKIE_SECURE=False/" .env
    
    echo "✅ .env file created with development settings"
fi

# Run migrations
echo "🔄 Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional)
read -p "Do you want to create a superuser? (y/n): " CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" = "y" ] || [ "$CREATE_SUPERUSER" = "Y" ]; then
    python manage.py createsuperuser
fi

echo "🎉 Setup complete!"
echo "✅ To start the development server, run:"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   python manage.py runserver"
echo ""
echo "🌐 Your College Management Portal will be available at: http://127.0.0.1:8000"
