#!/usr/bin/env python3
"""
Test login functionality
"""

import requests
import json

def test_login():
    """Test login API"""
    print("🔍 Testing login API...")
    
    try:
        # Test login endpoint
        login_data = {
            "username": "admin",
            "password": "admin123456"
        }
        
        response = requests.post(
            "http://localhost:8000/auth/login", 
            json=login_data, 
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Token: {data.get('access_token', 'N/A')[:50]}...")
            print(f"User: {data.get('user', {}).get('username', 'N/A')}")
            return True
        else:
            print("❌ Login failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Certificate Management Portal...")
    print("=" * 50)
    
    # Test health first
    health_ok = test_health()
    print()
    
    # Test login
    login_ok = test_login()
    
    print("\n" + "=" * 50)
    if health_ok and login_ok:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")





