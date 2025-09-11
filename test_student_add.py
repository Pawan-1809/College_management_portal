import os
import sys
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from student_management_app.models import Courses, SessionYearModel, Students, CustomUser

# Test adding a student
def test_add_student():
    print("Testing student addition functionality...")
    
    # Get test data
    courses = Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    
    if not courses.exists():
        print("ERROR: No courses found in database!")
        return False
    
    if not sessions.exists():
        print("ERROR: No session years found in database!")
        return False
    
    # Use first course and session for testing
    test_course = courses.first()
    test_session = sessions.first()
    
    print(f"Using Course: {test_course.course_name} (ID: {test_course.id})")
    print(f"Using Session: {test_session.session_start_year} to {test_session.session_end_year} (ID: {test_session.id})")
    
    # Create test student data
    test_data = {
        'username': 'teststudent123',
        'email': 'teststudent123@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'Student',
    }
    
    try:
        # Check if user already exists
        if CustomUser.objects.filter(username=test_data['username']).exists():
            print(f"User {test_data['username']} already exists. Deleting...")
            CustomUser.objects.filter(username=test_data['username']).delete()
        
        # Create user with user_type=3 (Student)
        print("Creating user...")
        user = CustomUser.objects.create_user(
            username=test_data['username'],
            email=test_data['email'],
            password=test_data['password'],
            first_name=test_data['first_name'],
            last_name=test_data['last_name'],
            user_type=3
        )
        user.save()
        print(f"User created successfully: {user.username}")
        
        # The Student object should be created automatically via signal
        # Let's verify and update it
        print("Checking student profile...")
        try:
            student = user.students
            print(f"Student profile found: ID {student.id}")
            
            # Update student details
            student.address = "123 Test Street"
            student.course_id = test_course
            student.session_year_id = test_session
            student.gender = "Male"
            student.profile_pic = ""
            student.save()
            
            print("Student details updated successfully!")
            
            # Verify the save
            saved_student = Students.objects.get(admin=user)
            print(f"\nVerification:")
            print(f"  - Student ID: {saved_student.id}")
            print(f"  - User: {saved_student.admin.username}")
            print(f"  - Email: {saved_student.admin.email}")
            print(f"  - Course: {saved_student.course_id.course_name}")
            print(f"  - Session: {saved_student.session_year_id.session_start_year} to {saved_student.session_year_id.session_end_year}")
            print(f"  - Address: {saved_student.address}")
            print(f"  - Gender: {saved_student.gender}")
            
            print("\n✅ Student addition test PASSED!")
            return True
            
        except Students.DoesNotExist:
            print("ERROR: Student profile was not created automatically!")
            print("This indicates an issue with the Django signals.")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR during student creation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_add_student()
    if not success:
        print("\n⚠️  The test failed. The 'Failed to add student' error is likely due to:")
        print("1. Missing or incorrect Django signal configuration")
        print("2. Database constraint violations")
        print("3. Form validation issues")
        print("\nCheck the error messages above for specific details.")
    else:
        print("\n✅ All tests passed! The student addition functionality is working correctly.")
