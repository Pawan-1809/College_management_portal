# 🚀 Heroku Deployment Steps - College Management Portal

## Step 1: Install Heroku CLI ✅ (Required)

1. **Download Heroku CLI:**
   - Visit: https://devcenter.heroku.com/articles/heroku-cli
   - Download the Windows installer
   - Install and restart your terminal

2. **Verify Installation:**
   ```bash
   heroku --version
   ```

## Step 2: Login to Heroku

```bash
heroku login
```
This will open your browser for authentication.

## Step 3: Create Heroku Application

```bash
# Replace 'your-app-name' with your desired app name (must be unique)
heroku create your-college-portal-app

# Or let Heroku generate a random name:
heroku create
```

## Step 4: Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

## Step 5: Set Environment Variables

Generate a secret key first:
```bash
python generate-secret-key.py
```

Then set the environment variables:
```bash
# Replace with your generated secret key
heroku config:set SECRET_KEY="your-generated-secret-key-here"

heroku config:set DEBUG=False

# Replace with your actual Heroku app URL
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"

# Optional: Set additional security flags
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set CSRF_COOKIE_SECURE=True
```

## Step 6: Deploy to Heroku

```bash
git push heroku main
```

## Step 7: Run Database Migrations

```bash
heroku run python manage.py migrate
```

## Step 8: Create Superuser (Admin)

```bash
heroku run python manage.py createsuperuser
```
Follow the prompts to create an admin account.

## Step 9: Open Your Application

```bash
heroku open
```

## Step 10: Verify Deployment

1. Visit your app URL
2. Try accessing `/admin` with your superuser credentials
3. Test the main functionality

---

## 🔧 Troubleshooting

### If deployment fails:

1. **Check logs:**
   ```bash
   heroku logs --tail
   ```

2. **Common issues:**
   - Missing environment variables
   - Database connection issues
   - Static files not loading

3. **Fix static files:**
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

### Environment Variables Reference:

```bash
# View all config vars
heroku config

# Set a config var
heroku config:set VARIABLE_NAME=value

# Remove a config var
heroku config:unset VARIABLE_NAME
```

---

## 📝 Quick Commands Summary

```bash
# Essential deployment commands
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY="your-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app.herokuapp.com"
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku open
```

---

## 🎉 Success!

Once completed, your College Management Portal will be live at:
`https://your-app-name.herokuapp.com`

### Default Login Credentials (if using demo data):
- **Admin:** admin@gmail.com / admin
- **Staff:** staff@gmail.com / staff  
- **Student:** student@gmail.com / student

**Note:** It's recommended to create new credentials for production use.

---

## 🔄 Future Updates

To update your deployed application:
```bash
git add .
git commit -m "Your update message"
git push heroku main
```

For database changes:
```bash
git push heroku main
heroku run python manage.py migrate
```
