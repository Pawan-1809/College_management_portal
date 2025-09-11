web: gunicorn student_management_system.wsgi --log-file -
release: python manage.py collectstatic --noinput && python manage.py migrate
