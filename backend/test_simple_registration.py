#!/usr/bin/env python3
"""
Simple registration test
"""

import requests
import json

def test_simple_registration():
    """Test simple registration"""
    print("🔍 Testing simple registration...")
    
    # Test with a simple email
    registration_data = {
        "full_name": "Test User 2",
        "email": "test2@example.com",
        "username": "testuser2",
        "password": "password123",
        "role": "student",
        "department": "engineering",
        "student_id": "02",
        "phone_number": "1234567890"
    }
    
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

if __name__ == "__main__":
    test_simple_registration()





