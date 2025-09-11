import os
import sys
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import Courses, SessionYearModel

# Check existing data
courses_count = Courses.objects.count()
sessions_count = SessionYearModel.objects.count()

print(f"Current Courses: {courses_count}")
print(f"Current Session Years: {sessions_count}")

# Add courses if none exist
if courses_count == 0:
    print("\nAdding sample courses...")
    courses_to_add = [
        "Computer Science",
        "Information Technology", 
        "Electronics Engineering",
        "Mechanical Engineering",
        "Civil Engineering"
    ]
    
    for course_name in courses_to_add:
        course = Courses(course_name=course_name)
        course.save()
        print(f"Added course: {course_name}")
    
    print(f"Total courses added: {len(courses_to_add)}")

# Add session years if none exist  
if sessions_count == 0:
    print("\nAdding sample session years...")
    sessions_to_add = [
        (date(2023, 1, 1), date(2023, 12, 31)),
        (date(2024, 1, 1), date(2024, 12, 31)),
        (date(2025, 1, 1), date(2025, 12, 31))
    ]
    
    for start_date, end_date in sessions_to_add:
        session = SessionYearModel(
            session_start_year=start_date,
            session_end_year=end_date
        )
        session.save()
        print(f"Added session: {start_date.year} to {end_date.year}")
    
    print(f"Total sessions added: {len(sessions_to_add)}")

# Verify the data
print("\n=== Final Database Status ===")
print(f"Total Courses: {Courses.objects.count()}")
print(f"Total Session Years: {SessionYearModel.objects.count()}")

# List all courses
print("\nAvailable Courses:")
for course in Courses.objects.all():
    print(f"  - ID: {course.id}, Name: {course.course_name}")

# List all session years
print("\nAvailable Session Years:")
for session in SessionYearModel.objects.all():
    print(f"  - ID: {session.id}, Period: {session.session_start_year} to {session.session_end_year}")
