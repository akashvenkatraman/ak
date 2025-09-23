#!/usr/bin/env python3
"""Complete login test with approved user"""

import requests
import json
from app.core.database import SessionLocal
from sqlalchemy import text
from app.core.auth import get_password_hash

def create_approved_user():
    """Create an approved test user"""
    try:
        db = SessionLocal()
        
        # Check if test user exists
        result = db.execute(text("SELECT id FROM users WHERE username = 'testuser'"))
        user = result.fetchone()
        
        if user:
            # Update user to approved status
            db.execute(text("UPDATE users SET status = 'APPROVED' WHERE username = 'testuser'"))
            db.commit()
            print("✅ Updated existing test user to approved status")
        else:
            # Create new approved user
            hashed_password = get_password_hash("testpass123")
            
            db.execute(text("""
                INSERT INTO users (email, username, full_name, hashed_password, role, status, is_active, phone_number, department, student_id, created_at)
                VALUES (:email, :username, :full_name, :hashed_password, :role, :status, :is_active, :phone_number, :department, :student_id, datetime('now'))
            """), {
                "email": "test@example.com",
                "username": "testuser",
                "full_name": "Test User",
                "hashed_password": hashed_password,
                "role": "STUDENT",
                "status": "APPROVED",
                "is_active": True,
                "phone_number": "1234567890",
                "department": "Computer Science",
                "student_id": "STU001"
            })
            
            db.commit()
            print("✅ Created new approved test user")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ User creation error: {e}")
        return False

def test_complete_login_flow():
    """Test complete login flow"""
    print("=== Complete Login Flow Test ===")
    
    # Create approved user
    if not create_approved_user():
        return False
    
    # Test login
    try:
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        print("🔐 Testing login...")
        response = requests.post("http://localhost:8000/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Token: {data.get('access_token', 'No token')[:50]}...")
            print(f"User: {data.get('user', {}).get('username', 'No user')}")
            print(f"Role: {data.get('user', {}).get('role', 'No role')}")
            print(f"Status: {data.get('user', {}).get('status', 'No status')}")
            
            # Test protected endpoint
            token = data.get('access_token')
            headers = {"Authorization": f"Bearer {token}"}
            
            print("🔐 Testing protected endpoint...")
            me_response = requests.get("http://localhost:8000/auth/me", headers=headers)
            print(f"Me endpoint response: {me_response.status_code}")
            
            if me_response.status_code == 200:
                print("✅ Protected endpoint access successful!")
                return True
            else:
                print(f"❌ Protected endpoint failed: {me_response.text}")
                return False
        else:
            print(f"❌ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False

def test_admin_login():
    """Test admin login"""
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        print("🔐 Testing admin login...")
        response = requests.post("http://localhost:8000/auth/login", json=login_data)
        print(f"Admin login response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful!")
            print(f"Admin role: {data.get('user', {}).get('role', 'No role')}")
            return True
        else:
            print(f"❌ Admin login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Admin login error: {e}")
        return False

def test_api_health():
    """Test API health"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check response: {response.status_code}")
        if response.status_code == 200:
            print("✅ API is healthy")
            return True
        else:
            print("❌ API health check failed")
            return False
    except Exception as e:
        print(f"❌ API health check error: {e}")
        return False

if __name__ == "__main__":
    print("=== Complete Login Test Suite ===")
    
    # Test API health
    if not test_api_health():
        print("❌ API not running, please start the backend server")
        exit(1)
    
    # Test admin login
    test_admin_login()
    
    # Test complete user login flow
    if test_complete_login_flow():
        print("🎉 All login tests passed!")
    else:
        print("❌ Some login tests failed")
    
    print("=== Test Complete ===")
