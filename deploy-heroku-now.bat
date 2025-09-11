@echo off
echo 🚀 Starting Heroku Deployment for College Management Portal...
echo.

:: Check if Heroku CLI is installed
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI is not installed!
    echo Please install it from: https://devcenter.heroku.com/articles/heroku-cli
    echo After installation, restart this script.
    pause
    exit /b 1
)

echo ✅ Heroku CLI found!
echo.

:: Login to Heroku
echo 🔐 Logging into Heroku...
heroku auth:whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Please login to Heroku:
    heroku login
    if %errorlevel% neq 0 (
        echo ❌ Login failed
        pause
        exit /b 1
    )
)

echo ✅ Logged into Heroku!
echo.

:: Get app name from user
set /p APP_NAME="Enter your app name (or press Enter for auto-generated): "

:: Create Heroku app
echo 📱 Creating Heroku app...
if "%APP_NAME%"=="" (
    heroku create
) else (
    heroku create %APP_NAME%
)

if %errorlevel% neq 0 (
    echo ❌ Failed to create app. It might already exist.
    pause
    exit /b 1
)

:: Add PostgreSQL
echo 🐘 Adding PostgreSQL database...
heroku addons:create heroku-postgresql:hobby-dev

:: Set environment variables
echo 🔧 Setting environment variables...
heroku config:set SECRET_KEY="To^3IFJpRTt14g6Mv04Xd#IBfGr1gvgEiHCSyzr6f39JLypBpr"
heroku config:set DEBUG=False

:: Get app URL for ALLOWED_HOSTS
for /f "tokens=*" %%i in ('heroku info -s ^| findstr "web_url"') do set APP_URL=%%i
set APP_URL=%APP_URL:web_url=%
set APP_URL=%APP_URL:https://=%
set APP_URL=%APP_URL:/=%

heroku config:set ALLOWED_HOSTS="%APP_URL%"

:: Deploy
echo 🚢 Deploying to Heroku...
git push heroku main

if %errorlevel% neq 0 (
    echo ❌ Deployment failed. Check the logs above.
    pause
    exit /b 1
)

:: Run migrations
echo 🔄 Running database migrations...
heroku run python manage.py migrate

:: Ask about superuser
echo.
set /p CREATE_SUPERUSER="Do you want to create a superuser? (y/n): "
if /i "%CREATE_SUPERUSER%"=="y" (
    heroku run python manage.py createsuperuser
)

:: Open the app
echo 🎉 Deployment complete!
echo Opening your College Management Portal...
heroku open

echo.
echo ✅ Your College Management Portal is now live on Heroku!
echo 📋 Check HEROKU_DEPLOYMENT_STEPS.md for detailed instructions
pause
