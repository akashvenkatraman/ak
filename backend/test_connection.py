#!/usr/bin/env python3
"""
Test script to verify backend and database connectivity
"""

import requests
import time
from app.core.database import engine, SessionLocal
from app.models.user import User
from sqlalchemy import text

def test_database():
    """Test database connection"""
    print("🔍 Testing database connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.fetchone()[0]
            print(f"✅ Database connected! Found {count} users")
            
            # Check if admin exists
            admin = conn.execute(text("SELECT username, email, role, status FROM users WHERE role = 'admin'")).fetchone()
            if admin:
                print(f"✅ Admin user found: {admin[0]} ({admin[1]}) - Role: {admin[2]}, Status: {admin[3]}")
            else:
                print("❌ No admin user found!")
            return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_backend():
    """Test backend API"""
    print("🔍 Testing backend API...")
    try:
        # Test root endpoint
        response = requests.get("http://localhost:8000", timeout=5)
        print(f"✅ Root endpoint: {response.status_code} - {response.text}")
        
        # Test auth endpoint
        response = requests.get("http://localhost:8000/auth/me", timeout=5)
        print(f"✅ Auth endpoint: {response.status_code}")
        
        # Test login endpoint
        login_data = {
            "username": "admin",
            "password": "admin123456"
        }
        response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=10)
        print(f"✅ Login endpoint: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login successful!")
        else:
            print(f"❌ Login failed: {response.text}")
        
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running!")
        return False
    except requests.exceptions.Timeout:
        print("❌ Backend request timed out!")
        return False
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Certificate Management Portal connectivity...")
    print("=" * 60)
    
    # Test database
    db_ok = test_database()
    
    # Test backend
    backend_ok = test_backend()
    
    print("\n" + "=" * 60)
    if db_ok and backend_ok:
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return db_ok and backend_ok

if __name__ == "__main__":
    main()





