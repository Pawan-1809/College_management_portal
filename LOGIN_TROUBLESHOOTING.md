# 🔐 Login Troubleshooting Guide

## Default Admin Credentials
- **Email/Username**: `admin@college.edu`
- **Password**: `admin123`

## Common Login Issues & Solutions

### 1. **Login Page Not Found**
- **URL**: Make sure you're accessing `/admin/` or the correct login URL
- **Example**: `https://your-app-name.onrender.com/admin/`

### 2. **"Invalid Login" Error**
This system uses **EMAIL** for authentication, not username.

#### ✅ Correct Login:
- **Username field**: Enter `admin@college.edu` (use the email)
- **Password field**: Enter `admin123`

#### ❌ Common Mistakes:
- Using just `admin` as username
- Case sensitivity issues
- Extra spaces in email/password

### 3. **User Not Found Error**
If the superuser wasn't created properly:

#### Check User Creation:
1. Go to your Render service dashboard
2. Click on "Shell" 
3. Run: `python manage.py list_users`
4. This will show all users in the system

#### Manually Create Superuser:
If no users exist, create one manually:
```bash
python manage.py create_default_superuser
```

### 4. **Authentication Backend Issues**
This system uses a custom email authentication backend:
- File: `student_management_app/EmailBackEnd.py`
- It authenticates using email instead of username
- Both username and email fields should contain the same email address

### 5. **User Type Issues**
The system has 3 user types:
- **1** = HOD (Admin) - Can access admin panel
- **2** = Staff - Limited admin access
- **3** = Student - No admin access

Make sure the default admin has `user_type=1`.

## Testing Login

### Step 1: Verify User Exists
```bash
# In Render shell
python manage.py list_users
```

Expected output should show:
```
Username: admin@college.edu
Email: admin@college.edu
Status: ✅ Active
Type: 👑 Superuser - HOD
```

### Step 2: Test Authentication
```bash
# In Render shell
python manage.py shell

# Then run:
from django.contrib.auth import authenticate
user = authenticate(username='admin@college.edu', password='admin123')
print(f"Authenticated user: {user}")
```

### Step 3: Access Admin Panel
1. Go to: `https://your-app-name.onrender.com/admin/`
2. Enter `admin@college.edu` in username field
3. Enter `admin123` in password field
4. Click "Log in"

## Reset Admin Password

If you need to reset the password:

```bash
# In Render shell
python manage.py shell

# Then run:
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(email='admin@college.edu')
user.set_password('newpassword123')
user.save()
print("Password updated!")
```

## Create Additional Admin Users

```bash
# In Render shell
python manage.py shell

# Then run:
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser(
    username='newadmin@college.edu',
    email='newadmin@college.edu', 
    password='newpassword123',
    first_name='New',
    last_name='Admin',
    user_type=1
)
```

## Security Reminder

⚠️ **IMPORTANT**: After first successful login:
1. Change the default password immediately
2. Consider creating additional admin accounts
3. Remove or disable the default account for production use

## Still Having Issues?

1. Check Render application logs for authentication errors
2. Verify the application is running properly
3. Make sure migrations have been applied
4. Confirm the CustomUser model is working correctly

---

**Need help?** Check the application logs in your Render dashboard for specific error messages.
