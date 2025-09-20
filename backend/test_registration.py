#!/usr/bin/env python3
"""
Test registration functionality
"""

import requests
import json

def test_registration():
    """Test registration API"""
    print("🔍 Testing registration API...")
    
    try:
        # Test registration endpoint
        registration_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "role": "student",
            "department": "engineering",
            "student_id": "12345",
            "phone_number": "1234567890"
        }
        
        response = requests.post(
            "http://localhost:8000/auth/register", 
            json=registration_data, 
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Registration successful!")
            print(f"User: {data.get('username', 'N/A')}")
            return True
        else:
            print("❌ Registration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        from app.core.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.fetchone()[0]
            print(f"✅ Database connected! Users count: {count}")
            return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Registration System...")
    print("=" * 50)
    
    # Test database first
    db_ok = test_database_connection()
    print()
    
    # Test registration
    reg_ok = test_registration()
    
    print("\n" + "=" * 50)
    if db_ok and reg_ok:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")





