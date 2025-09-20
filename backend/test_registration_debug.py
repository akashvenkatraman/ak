#!/usr/bin/env python3
"""
Debug registration issues
"""

import requests
import json
import time

def test_registration_with_fresh_data():
    """Test registration with fresh data"""
    print("🔍 Testing Registration with Fresh Data...")
    
    # Generate unique email
    timestamp = int(time.time())
    email = f"debug{timestamp}@example.com"
    username = f"debug{timestamp}"
    
    registration_data = {
        "full_name": "Debug User",
        "email": email,
        "username": username,
        "password": "password123",
        "role": "student",
        "department": "engineering",
        "student_id": "99",
        "phone_number": "9876543210"
    }
    
    print(f"Testing with email: {email}")
    print(f"Testing with username: {username}")
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/register", 
            json=registration_data, 
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Registration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_endpoint():
    """Test health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_database_health():
    """Test database health"""
    print("\n🔍 Testing Database Health...")
    
    try:
        response = requests.get("http://localhost:8000/health/database", timeout=5)
        print(f"Database Status: {response.status_code}")
        print(f"Database Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Database health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Debugging Registration Issues...")
    print("=" * 50)
    
    # Test health first
    health_ok = test_health_endpoint()
    db_ok = test_database_health()
    
    # Test registration
    reg_ok = test_registration_with_fresh_data()
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"Health Check: {'✅' if health_ok else '❌'}")
    print(f"Database Check: {'✅' if db_ok else '❌'}")
    print(f"Registration: {'✅' if reg_ok else '❌'}")
    
    if not reg_ok:
        print("\n🔧 Registration is failing. Let's check the server logs...")





