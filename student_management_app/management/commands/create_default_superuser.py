from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Create a default superuser for initial deployment'

    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            # Check if any superuser exists
            if User.objects.filter(is_superuser=True).exists():
                self.stdout.write(
                    self.style.SUCCESS('ℹ️  Superuser already exists - skipping creation')
                )
                return
            
            # Create default superuser
            user = User.objects.create_superuser(
                email='admin@college.edu',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Default superuser created successfully!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: admin@college.edu')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Password: admin123')
            )
            self.stdout.write(
                self.style.WARNING('⚠️  Please change this password after first login!')
            )
            
        except IntegrityError as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️  User might already exist: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {e}')
            )
            raise
