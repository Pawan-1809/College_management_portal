# Render Deployment Guide for College Management Portal

## 🚀 Quick Deployment Steps

### Prerequisites
- GitHub account
- Render account (free tier available)
- Your code pushed to a GitHub repository

### Step 1: Create PostgreSQL Database on Render

1. Log into your Render dashboard
2. Click **"New"** → **"PostgreSQL"**
3. Fill in the details:
   - **Name**: `college-portal-db`
   - **Database**: `college_management_db`
   - **User**: `college_user`
   - **Region**: Choose closest to your location
   - **Plan**: `Free` (for testing/development)
4. Click **"Create Database"**
5. Wait for the database to be created and note the connection details

### Step 2: Create Web Service

1. In Render dashboard, click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Fill in the service details:
   - **Name**: `college-management-portal`
   - **Region**: Same as your database
   - **Branch**: `main` (or your default branch)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn student_management_system.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: `Free`

### Step 3: Set Environment Variables

In your Web Service settings, go to the **Environment** tab and add these variables:

#### Required Variables
```
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
DATABASE_URL=postgresql://user:password@host:port/database
```

#### Optional Variables (for production)
```
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**Note**: The SSL redirect settings are set to `False` because Render handles SSL termination at the edge.

### Step 4: Link Database (Alternative Method)

If you're using the `render.yaml` file (which is included in this project):

1. The database will be automatically created and linked
2. Environment variables will be automatically set
3. Just push your code to trigger deployment

### Step 5: Deploy

1. Click **"Create Web Service"** or **"Deploy"**
2. Watch the build logs in the Render dashboard
3. The deployment process will:
   - Install Python dependencies
   - Collect static files
   - Run database migrations
   - Create a default admin user (email: `admin@college.edu`, password: `admin123`)

### Step 6: Access Your Application

1. Once deployment is successful, you'll get a URL like: `https://your-service-name.onrender.com`
2. Visit the URL to see your application
3. Access the admin panel at: `https://your-service-name.onrender.com/admin/`

## 🔧 Configuration Details

### Database Configuration
- **Engine**: PostgreSQL (production-ready)
- **Connection**: Handled via `DATABASE_URL` environment variable
- **Migrations**: Automatically run during build process

### Static Files
- **Storage**: WhiteNoise (for serving static files)
- **Collection**: Automatic during build process
- **URL**: `/static/`

### Admin Access
A default superuser is created with:
- **Email**: `admin@college.edu`
- **Password**: `admin123`

**⚠️ Important**: Change this password immediately after first login!

## 🐛 Troubleshooting

### Common Issues

1. **Build Fails with Python Version Error**
   - Render uses Python 3.11.10 as specified in `runtime.txt`
   - If you see version conflicts, check `requirements.txt`

2. **Database Connection Error**
   - Verify `DATABASE_URL` is correctly set
   - Ensure the PostgreSQL database is running
   - Check that the database and web service are in the same region

3. **Static Files Not Loading**
   - Check if `collectstatic` ran successfully in build logs
   - Verify `STATIC_ROOT` and `STATIC_URL` settings in `settings.py`

4. **Admin User Creation Fails**
   - Check build logs for any errors during user creation
   - Manually create a superuser using Render's shell feature:
     ```bash
     python manage.py createsuperuser
     ```

### Viewing Logs
- Go to your Web Service in Render dashboard
- Click on **"Logs"** tab to see real-time application logs
- Use **"Events"** tab to see deployment history

### Using Render Shell
1. In your Web Service dashboard, click **"Shell"**
2. Run Django management commands:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

## 🔒 Security Considerations

### For Production Use:
1. **Change Default Admin Password**
   - Login to admin panel immediately
   - Change the default password

2. **Environment Variables**
   - Use strong, unique `SECRET_KEY`
   - Set `DEBUG=False`
   - Configure proper `ALLOWED_HOSTS`

3. **Database Backup**
   - Render Free PostgreSQL doesn't include automated backups
   - Consider upgrading to a paid plan for production use
   - Manually backup important data regularly

4. **SSL/HTTPS**
   - Render automatically provides SSL certificates
   - Your app will be served over HTTPS
   - No additional configuration needed

## 📊 Monitoring

### Health Checks
- Render automatically performs health checks on `/`
- Monitor uptime in the Render dashboard

### Performance
- Free tier has limitations (512MB RAM, sleeps after inactivity)
- Consider upgrading for production workloads

## 🔄 Updates and Maintenance

### Deploying Updates
1. Push changes to your GitHub repository
2. Render will automatically detect changes and redeploy
3. Monitor the build process in the dashboard

### Manual Deployment
- In your Web Service dashboard, click **"Manual Deploy"**
- Select the branch to deploy

### Database Migrations
- New migrations run automatically during deployment
- For manual migrations, use the Render shell

## 💡 Tips

1. **Development vs Production**
   - Use different Render services for staging and production
   - Test changes in staging before deploying to production

2. **Environment Variables**
   - Keep sensitive data in environment variables
   - Never commit secrets to your repository

3. **Logs**
   - Regularly check logs for errors or performance issues
   - Set up log monitoring for production apps

4. **Backup Strategy**
   - Export your database regularly
   - Keep backups of uploaded media files

## 📞 Support

### If you encounter issues:
1. Check the build and application logs in Render dashboard
2. Verify all environment variables are set correctly
3. Test the application locally with the same settings
4. Check Render's status page for platform issues
5. Consult Render's documentation for specific error messages

### Useful Resources
- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [PostgreSQL on Render](https://render.com/docs/databases)

---

**🎉 Congratulations!** Your College Management Portal is now deployed on Render and ready for use!
