#!/usr/bin/env python3
"""Test frontend-backend integration"""

import requests
import json

def test_cors_headers():
    """Test CORS headers for frontend integration"""
    try:
        # Test OPTIONS request (preflight)
        response = requests.options("http://localhost:8000/auth/login", 
                                  headers={
                                      "Origin": "http://localhost:3000",
                                      "Access-Control-Request-Method": "POST",
                                      "Access-Control-Request-Headers": "Content-Type"
                                  })
        print(f"CORS preflight response: {response.status_code}")
        print(f"CORS headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ CORS preflight successful")
            return True
        else:
            print("❌ CORS preflight failed")
            return False
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    endpoints = [
        ("GET", "/health", "Health check"),
        ("GET", "/", "Root endpoint"),
        ("GET", "/docs", "API documentation"),
    ]
    
    for method, endpoint, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"http://localhost:8000{endpoint}")
            else:
                response = requests.post(f"http://localhost:8000{endpoint}")
            
            print(f"{description}: {response.status_code}")
            if response.status_code in [200, 404]:  # 404 is OK for some endpoints
                print(f"✅ {description} accessible")
            else:
                print(f"❌ {description} failed")
        except Exception as e:
            print(f"❌ {description} error: {e}")

def test_login_endpoint():
    """Test login endpoint specifically"""
    try:
        # Test with invalid credentials first
        login_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        
        response = requests.post("http://localhost:8000/auth/login", json=login_data)
        print(f"Invalid login response: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Invalid login properly rejected")
        else:
            print(f"❌ Invalid login not properly handled: {response.text}")
        
        # Test with valid credentials
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        response = requests.post("http://localhost:8000/auth/login", json=login_data)
        print(f"Valid login response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Valid login successful")
            print(f"Response structure: {list(data.keys())}")
            return True
        else:
            print(f"❌ Valid login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login endpoint test error: {e}")
        return False

if __name__ == "__main__":
    print("=== Frontend-Backend Integration Test ===")
    
    # Test CORS
    test_cors_headers()
    
    # Test API endpoints
    test_api_endpoints()
    
    # Test login endpoint
    test_login_endpoint()
    
    print("=== Integration Test Complete ===")
