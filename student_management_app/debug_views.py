from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json


def debug_list_users(request):
    """List all users - for debugging login issues"""
    User = get_user_model()
    
    users = User.objects.all()
    user_list = []
    
    for user in users:
        user_info = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'user_type': user.user_type,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        }
        user_list.append(user_info)
    
    html = f"""
    <html>
    <head>
        <title>User Debug Info</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .user {{ background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .superuser {{ background: #e8f5e8; border-left: 4px solid #4caf50; }}
            .inactive {{ background: #ffe8e8; border-left: 4px solid #f44336; }}
            .actions {{ margin: 20px 0; }}
            .action-btn {{ 
                display: inline-block; 
                padding: 10px 20px; 
                margin: 5px; 
                background: #007cba; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
            }}
            .danger {{ background: #dc3545; }}
            .success {{ background: #28a745; }}
        </style>
    </head>
    <body>
        <h1>🔐 User Debug Information</h1>
        <p><strong>Total Users:</strong> {len(user_list)}</p>
        
        <div class="actions">
            <a href="/debug/create-admin/" class="action-btn success">Create Admin User</a>
            <a href="/debug/test-auth/" class="action-btn">Test Authentication</a>
            <a href="/debug/reset-admin/" class="action-btn danger">Reset Admin Password</a>
        </div>
        
        <h2>👥 All Users:</h2>
    """
    
    if not user_list:
        html += "<p><strong>❌ No users found in the system!</strong></p>"
    
    for user in user_list:
        css_class = "user"
        if user['is_superuser']:
            css_class += " superuser"
        if not user['is_active']:
            css_class += " inactive"
            
        status = "✅ Active" if user['is_active'] else "❌ Inactive"
        superuser = "👑 Superuser" if user['is_superuser'] else "👤 Regular User"
        user_types = {1: "HOD/Admin", 2: "Staff", 3: "Student"}
        user_type_name = user_types.get(int(user['user_type']), "Unknown")
        
        html += f"""
        <div class="{css_class}">
            <strong>Username:</strong> {user['username']}<br>
            <strong>Email:</strong> {user['email']}<br>
            <strong>Name:</strong> {user['first_name']} {user['last_name']}<br>
            <strong>Status:</strong> {status}<br>
            <strong>Type:</strong> {superuser} - {user_type_name} (Code: {user['user_type']})<br>
            <strong>Joined:</strong> {user['date_joined']}<br>
        </div>
        """
    
    html += """
        <h2>🔑 Login Instructions:</h2>
        <div style="background: #e3f2fd; padding: 15px; border-radius: 5px;">
            <p><strong>Admin Login URL:</strong> <a href="/admin/">/admin/</a></p>
            <p><strong>Expected Credentials:</strong></p>
            <ul>
                <li>Username: admin@college.edu</li>
                <li>Password: admin123</li>
            </ul>
            <p><strong>Note:</strong> This system uses EMAIL for authentication, not username!</p>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html)


@csrf_exempt
def debug_create_admin(request):
    """Create admin user via web interface"""
    User = get_user_model()
    
    try:
        # Check if admin already exists
        existing_user = User.objects.filter(email='admin@college.edu').first()
        if existing_user:
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; margin: 20px;">
                <h1>⚠️ Admin User Already Exists</h1>
                <p><strong>Found existing user:</strong></p>
                <ul>
                    <li>Username: {existing_user.username}</li>
                    <li>Email: {existing_user.email}</li>
                    <li>Is Superuser: {existing_user.is_superuser}</li>
                    <li>User Type: {existing_user.user_type}</li>
                </ul>
                <p><a href="/debug/reset-admin/">Reset Password</a> | <a href="/debug/list-users/">Back to User List</a></p>
            </body>
            </html>
            """
            return HttpResponse(html)
        
        # Create new admin user
        user = User.objects.create_superuser(
            username='admin@college.edu',
            email='admin@college.edu',
            password='admin123',
            first_name='Admin',
            last_name='User',
            user_type=1  # HOD type
        )
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h1>✅ Admin User Created Successfully!</h1>
            <div style="background: #e8f5e8; padding: 15px; border-radius: 5px;">
                <p><strong>Created User:</strong></p>
                <ul>
                    <li>Username: {user.username}</li>
                    <li>Email: {user.email}</li>
                    <li>Password: admin123</li>
                    <li>User Type: {user.user_type} (HOD/Admin)</li>
                    <li>Is Superuser: {user.is_superuser}</li>
                </ul>
            </div>
            <h2>🔑 Login Now:</h2>
            <p><a href="/admin/" style="display: inline-block; padding: 10px 20px; background: #007cba; color: white; text-decoration: none; border-radius: 5px;">Go to Admin Login</a></p>
            <p><a href="/debug/list-users/">View All Users</a></p>
        </body>
        </html>
        """
        return HttpResponse(html)
        
    except Exception as e:
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h1>❌ Error Creating Admin User</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <p><a href="/debug/list-users/">Back to User List</a></p>
        </body>
        </html>
        """
        return HttpResponse(html)


@csrf_exempt
def debug_test_auth(request):
    """Test authentication via web interface"""
    test_email = 'admin@college.edu'
    test_password = 'admin123'
    
    # Test authentication
    user = authenticate(username=test_email, password=test_password)
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 20px;">
        <h1>🔐 Authentication Test</h1>
        <p><strong>Testing credentials:</strong></p>
        <ul>
            <li>Username: {test_email}</li>
            <li>Password: {test_password}</li>
        </ul>
    """
    
    if user:
        html += f"""
        <div style="background: #e8f5e8; padding: 15px; border-radius: 5px;">
            <h2>✅ Authentication Successful!</h2>
            <p><strong>Authenticated User:</strong></p>
            <ul>
                <li>Username: {user.username}</li>
                <li>Email: {user.email}</li>
                <li>Is Superuser: {user.is_superuser}</li>
                <li>User Type: {user.user_type}</li>
                <li>Is Active: {user.is_active}</li>
            </ul>
        </div>
        <p>✅ <strong>Authentication works! You should be able to login.</strong></p>
        <p><a href="/admin/" style="display: inline-block; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px;">Try Admin Login Now</a></p>
        """
    else:
        html += f"""
        <div style="background: #ffe8e8; padding: 15px; border-radius: 5px;">
            <h2>❌ Authentication Failed!</h2>
            <p>The credentials admin@college.edu / admin123 do not work.</p>
        </div>
        <p><a href="/debug/create-admin/" style="display: inline-block; padding: 10px 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px;">Create Admin User</a></p>
        """
    
    html += """
        <p><a href="/debug/list-users/">Back to User List</a></p>
    </body>
    </html>
    """
    
    return HttpResponse(html)


@csrf_exempt
def debug_reset_admin(request):
    """Reset admin password via web interface"""
    User = get_user_model()
    
    try:
        user = User.objects.get(email='admin@college.edu')
        user.set_password('admin123')
        user.user_type = 1  # Ensure it's set to HOD
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h1>✅ Admin Password Reset Successfully!</h1>
            <div style="background: #e8f5e8; padding: 15px; border-radius: 5px;">
                <p><strong>Updated User:</strong></p>
                <ul>
                    <li>Username: {user.username}</li>
                    <li>Email: {user.email}</li>
                    <li>Password: admin123 (reset)</li>
                    <li>User Type: {user.user_type} (HOD/Admin)</li>
                    <li>Is Superuser: {user.is_superuser}</li>
                    <li>Is Active: {user.is_active}</li>
                </ul>
            </div>
            <p><a href="/admin/" style="display: inline-block; padding: 10px 20px; background: #007cba; color: white; text-decoration: none; border-radius: 5px;">Try Login Now</a></p>
            <p><a href="/debug/test-auth/">Test Authentication</a> | <a href="/debug/list-users/">Back to User List</a></p>
        </body>
        </html>
        """
        return HttpResponse(html)
        
    except User.DoesNotExist:
        html = """
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h1>❌ Admin User Not Found</h1>
            <p>No user with email admin@college.edu exists.</p>
            <p><a href="/debug/create-admin/">Create Admin User</a> | <a href="/debug/list-users/">Back to User List</a></p>
        </body>
        </html>
        """
        return HttpResponse(html)
    except Exception as e:
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h1>❌ Error Resetting Password</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <p><a href="/debug/list-users/">Back to User List</a></p>
        </body>
        </html>
        """
        return HttpResponse(html)
