# College Management Portal - Deployment Guide

This guide provides comprehensive instructions for deploying the College Management Portal across different platforms.

## 📋 Prerequisites

- Python 3.9 or higher
- Git
- PostgreSQL (for production)
- Docker & Docker Compose (for containerized deployment)
- Heroku CLI (for Heroku deployment)

## 🚀 Quick Deployment Options

### 1. Heroku Deployment (Recommended for beginners)

#### Step 1: Prepare Your Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd College-management-portal-master

# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login
```

#### Step 2: Run Automated Deployment Script
```bash
chmod +x deploy-heroku.sh
./deploy-heroku.sh
```

#### Step 3: Manual Configuration (if not using script)
```bash
# Create Heroku app
heroku create your-app-name

# Add PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 2. Docker Deployment

#### Step 1: Install Docker
- Visit: https://docs.docker.com/get-docker/
- Install Docker Desktop for your operating system

#### Step 2: Run Automated Deployment
```bash
chmod +x deploy-docker.sh
./deploy-docker.sh
```

#### Step 3: Manual Docker Deployment
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Build and run
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 3. Traditional VPS/Server Deployment

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx -y

# Create application user
sudo adduser collegeapp
sudo usermod -aG sudo collegeapp
```

#### Step 2: Application Setup
```bash
# Switch to app user
sudo su - collegeapp

# Clone repository
git clone <your-repo-url>
cd College-management-portal-master

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env file with production settings
```

#### Step 3: Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE college_management_db;
CREATE USER collegeapp WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE college_management_db TO collegeapp;
\\q

# Run migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### Step 4: Configure Gunicorn
```bash
# Create Gunicorn service file
sudo nano /etc/systemd/system/collegeapp.service
```

Add the following content:
```ini
[Unit]
Description=College Management Portal
After=network.target

[Service]
User=collegeapp
Group=www-data
WorkingDirectory=/home/collegeapp/College-management-portal-master
Environment="PATH=/home/collegeapp/College-management-portal-master/venv/bin"
ExecStart=/home/collegeapp/College-management-portal-master/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/collegeapp/College-management-portal-master/collegeapp.sock student_management_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable service
sudo systemctl start collegeapp
sudo systemctl enable collegeapp
```

#### Step 5: Configure Nginx
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/collegeapp
```

Add the following content:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/collegeapp/College-management-portal-master;
    }

    location /media/ {
        root /home/collegeapp/College-management-portal-master;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/collegeapp/College-management-portal-master/collegeapp.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/collegeapp /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 🔧 Environment Variables

### Required Variables
- `SECRET_KEY`: Django secret key for cryptographic operations
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames
- `DB_ENGINE`: Database engine (django.db.backends.postgresql for production)
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port

### Security Variables (Production)
- `SECURE_SSL_REDIRECT`: Enable HTTPS redirect
- `SESSION_COOKIE_SECURE`: Secure session cookies
- `CSRF_COOKIE_SECURE`: Secure CSRF cookies

### Optional Variables
- `EMAIL_HOST`: SMTP server for email functionality
- `EMAIL_HOST_USER`: Email username
- `EMAIL_HOST_PASSWORD`: Email password
- `AWS_ACCESS_KEY_ID`: AWS credentials for S3 storage
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_STORAGE_BUCKET_NAME`: S3 bucket name

## 🔒 Security Checklist

### Before Deployment
- [ ] Generate a strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use PostgreSQL in production
- [ ] Enable SSL/HTTPS
- [ ] Set secure cookie flags
- [ ] Review and update dependencies
- [ ] Configure proper logging
- [ ] Set up database backups
- [ ] Configure monitoring

### SSL/HTTPS Setup
For production deployments, always use HTTPS:

#### Using Let's Encrypt (Free SSL)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your_domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🧪 Local Development

For local development and testing:

```bash
chmod +x setup-local.sh
./setup-local.sh
```

This will:
- Create virtual environment
- Install dependencies
- Set up development .env file
- Run migrations
- Collect static files
- Optionally create superuser

## 📊 Monitoring & Maintenance

### Health Check Endpoint
The application includes a health check endpoint at `/health/` for monitoring.

### Logs
- Application logs: Check `errors.log` in project root
- Gunicorn logs: `sudo journalctl -u collegeapp`
- Nginx logs: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`

### Database Backups
```bash
# Create backup
pg_dump -h localhost -U collegeapp college_management_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
psql -h localhost -U collegeapp college_management_db < backup_file.sql
```

## 🆘 Troubleshooting

### Common Issues

1. **Static files not loading**
   - Run `python manage.py collectstatic --noinput`
   - Check STATIC_ROOT and STATICFILES_DIRS settings

2. **Database connection errors**
   - Verify database credentials in .env
   - Ensure PostgreSQL is running
   - Check firewall settings

3. **Permission errors**
   - Check file permissions: `chown -R collegeapp:www-data /path/to/app`
   - Verify user has proper database permissions

4. **Import errors**
   - Activate virtual environment
   - Install missing dependencies: `pip install -r requirements.txt`

### Debug Mode
For troubleshooting, temporarily enable debug mode:
```bash
heroku config:set DEBUG=True  # For Heroku
# Or edit .env file for other deployments
```
**Remember to disable debug mode in production!**

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Verify environment variables
4. Check database connectivity

## 🔄 Updates & Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
sudo systemctl restart collegeapp  # For VPS
# Or redeploy to Heroku/Docker
```

---

**Note**: Always test deployments in a staging environment before deploying to production!
