#!/usr/bin/env python3
"""
Test CORS and frontend connectivity
"""

import requests
import json

def test_cors_preflight():
    """Test CORS preflight request"""
    print("🔍 Testing CORS Preflight Request...")
    
    try:
        # Test OPTIONS request (CORS preflight)
        response = requests.options(
            "http://localhost:8000/auth/register",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            },
            timeout=5
        )
        
        print(f"CORS OPTIONS Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        
        return response.status_code in [200, 204]
        
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def test_frontend_origin():
    """Test registration with frontend origin"""
    print("\n🔍 Testing Registration with Frontend Origin...")
    
    try:
        registration_data = {
            "full_name": "CORS Test User",
            "email": "cors@example.com",
            "username": "cors_test",
            "password": "password123",
            "role": "student",
            "department": "engineering",
            "student_id": "99",
            "phone_number": "1234567890"
        }
        
        response = requests.post(
            "http://localhost:8000/auth/register",
            json=registration_data,
            headers={
                "Origin": "http://localhost:3000",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"Response Headers: {dict(response.headers)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Frontend origin test failed: {e}")
        return False

def test_health_from_frontend():
    """Test health endpoint from frontend origin"""
    print("\n🔍 Testing Health from Frontend Origin...")
    
    try:
        response = requests.get(
            "http://localhost:8000/health",
            headers={
                "Origin": "http://localhost:3000"
            },
            timeout=5
        )
        
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing CORS and Frontend Connectivity...")
    print("=" * 60)
    
    cors_ok = test_cors_preflight()
    health_ok = test_health_from_frontend()
    reg_ok = test_frontend_origin()
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"CORS Preflight: {'✅' if cors_ok else '❌'}")
    print(f"Health Check: {'✅' if health_ok else '❌'}")
    print(f"Registration: {'✅' if reg_ok else '❌'}")
    
    if cors_ok and health_ok and reg_ok:
        print("\n🎉 Backend is working perfectly!")
        print("The issue is likely in the frontend browser cache or build.")
        print("\n🔧 Try these solutions:")
        print("1. Clear browser cache (Ctrl+Shift+R)")
        print("2. Open browser developer tools and check console for errors")
        print("3. Check Network tab to see the actual request being sent")
    else:
        print("\n🔧 Backend issues detected. Let's fix them...")





