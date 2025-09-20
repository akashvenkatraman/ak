#!/usr/bin/env python3
"""
Test frontend registration format
"""

import requests
import json
import time

def test_frontend_registration_format():
    """Test registration with frontend format"""
    print("🔍 Testing Frontend Registration Format...")
    
    # Generate unique email
    timestamp = int(time.time())
    email = f"frontend{timestamp}@example.com"
    username = f"frontend{timestamp}"
    
    # This is exactly what the frontend sends
    registration_data = {
        "full_name": "Akash V",
        "email": email,
        "username": username,
        "password": "password123",
        "role": "student",  # Frontend sends string, not enum
        "department": "engineering",
        "student_id": "01",
        "phone_number": "09092266566"
    }
    
    print(f"Testing with email: {email}")
    print(f"Testing with username: {username}")
    print(f"Registration data: {json.dumps(registration_data, indent=2)}")
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/register", 
            json=registration_data, 
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Frontend format registration successful!")
            return True
        else:
            print("❌ Frontend format registration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_teacher_registration():
    """Test teacher registration"""
    print("\n🔍 Testing Teacher Registration...")
    
    timestamp = int(time.time())
    email = f"teacher{timestamp}@example.com"
    username = f"teacher{timestamp}"
    
    registration_data = {
        "full_name": "Teacher Name",
        "email": email,
        "username": username,
        "password": "password123",
        "role": "teacher",
        "department": "engineering",
        "employee_id": "EMP001",
        "phone_number": "9876543210"
    }
    
    print(f"Testing teacher with email: {email}")
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/register", 
            json=registration_data, 
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Teacher registration successful!")
            return True
        else:
            print("❌ Teacher registration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Frontend Registration Format...")
    print("=" * 60)
    
    student_ok = test_frontend_registration_format()
    teacher_ok = test_teacher_registration()
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"Student Registration: {'✅' if student_ok else '❌'}")
    print(f"Teacher Registration: {'✅' if teacher_ok else '❌'}")
    
    if student_ok and teacher_ok:
        print("\n🎉 Both student and teacher registration working!")
        print("The issue might be in the frontend UI or browser cache.")
    else:
        print("\n🔧 Registration is still failing. Let's check the server logs...")





