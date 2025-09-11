#!/bin/bash
# Heroku Deployment Script for College Management Portal

echo "🚀 Starting Heroku Deployment..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first."
    echo "Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login to Heroku (if not already logged in)
echo "🔐 Checking Heroku authentication..."
heroku auth:whoami || heroku login

# Create Heroku app (you can customize the app name)
echo "📱 Creating Heroku app..."
read -p "Enter your app name (or press Enter for auto-generated): " APP_NAME

if [ -z "$APP_NAME" ]; then
    heroku create
else
    heroku create "$APP_NAME"
fi

# Add PostgreSQL addon
echo "🐘 Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
echo "🔧 Setting environment variables..."
echo "Please set your environment variables using:"
echo "heroku config:set SECRET_KEY=your-secret-key"
echo "heroku config:set DEBUG=False"
echo "heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com"

read -p "Press Enter to continue after setting environment variables..."

# Deploy to Heroku
echo "🚢 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run migrations
echo "🔄 Running database migrations..."
heroku run python manage.py migrate

# Create superuser (optional)
read -p "Do you want to create a superuser? (y/n): " CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" = "y" ] || [ "$CREATE_SUPERUSER" = "Y" ]; then
    heroku run python manage.py createsuperuser
fi

# Open the app
echo "🎉 Deployment complete!"
heroku open

echo "✅ Your College Management Portal is now live on Heroku!"
