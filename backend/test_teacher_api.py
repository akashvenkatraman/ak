#!/usr/bin/env python3
"""
Test script to debug teacher API and student allocation
"""

import requests
import json
from app.core.database import get_db
from app.models.user import User, TeacherStudentAllocation, UserStatus
from app.core.auth import create_access_token

def test_teacher_api():
    print("=== TESTING TEACHER API ===")
    
    # Get database connection
    db = next(get_db())
    
    # Get teacher
    teacher = db.query(User).filter(User.role == 'teacher').first()
    if not teacher:
        print("❌ No teacher found in database")
        return
    
    print(f"✅ Teacher found: {teacher.username} ({teacher.email})")
    
    # Create a test token with all required fields
    token = create_access_token(data={
        "sub": teacher.username,
        "user_id": teacher.id,
        "role": teacher.role.value
    })
    print(f"✅ Token created: {token[:50]}...")
    
    # Test the teachers/students endpoint
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get("http://localhost:8000/teachers/students", headers=headers)
        print(f"✅ API Response Status: {response.status_code}")
        print(f"✅ API Response: {response.text}")
        
        if response.status_code == 200:
            students = response.json()
            print(f"✅ Found {len(students)} allocated students")
            for student in students:
                print(f"  - {student.get('full_name')} ({student.get('email')})")
        else:
            print(f"❌ API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Check allocations directly
    print("\n=== CHECKING ALLOCATIONS DIRECTLY ===")
    allocations = db.query(TeacherStudentAllocation).filter(
        TeacherStudentAllocation.teacher_id == teacher.id
    ).all()
    
    print(f"✅ Found {len(allocations)} allocations for teacher {teacher.id}")
    
    for allocation in allocations:
        student = db.query(User).filter(User.id == allocation.student_id).first()
        if student:
            print(f"  - Student: {student.full_name} ({student.email}) - Status: {student.status}")
        else:
            print(f"  - Student ID {allocation.student_id} not found")

if __name__ == "__main__":
    test_teacher_api()
