from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student_management_system import settings
from student_management_app import debug_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('student_management_app.urls')),
    
    # Debug URLs (temporary for troubleshooting)
    path('debug/list-users/', debug_views.debug_list_users, name='debug_list_users'),
    path('debug/create-admin/', debug_views.debug_create_admin, name='debug_create_admin'),
    path('debug/test-auth/', debug_views.debug_test_auth, name='debug_test_auth'),
    path('debug/reset-admin/', debug_views.debug_reset_admin, name='debug_reset_admin'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

