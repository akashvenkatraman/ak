#!/usr/bin/env python3
"""Test login functionality"""

import requests
import json
from app.core.database import SessionLocal
from sqlalchemy import text

def test_database_connection():
    """Test if database is working"""
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT COUNT(*) FROM users"))
        count = result.fetchone()[0]
        print(f"✅ Database connected. Users count: {count}")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    try:
        # Test data
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User",
            "role": "student",
            "phone_number": "1234567890",
            "department": "Computer Science",
            "student_id": "STU001"
        }
        
        response = requests.post("http://localhost:8000/auth/register", json=user_data)
        print(f"Registration response: {response.status_code}")
        if response.status_code == 200:
            print("✅ User registered successfully")
            return True
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_user_login():
    """Test user login"""
    try:
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        response = requests.post("http://localhost:8000/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful")
            print(f"Token: {data.get('access_token', 'No token')[:50]}...")
            return True
        else:
            print(f"❌ Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def create_test_admin():
    """Create a test admin user"""
    try:
        db = SessionLocal()
        
        # Check if admin exists
        result = db.execute(text("SELECT id FROM users WHERE role = 'ADMIN'"))
        admin = result.fetchone()
        
        if admin:
            print("✅ Admin user already exists")
            db.close()
            return True
        
        # Create admin user
        from app.core.auth import get_password_hash
        hashed_password = get_password_hash("admin123")
        
        db.execute(text("""
            INSERT INTO users (email, username, full_name, hashed_password, role, status, is_active, created_at)
            VALUES (:email, :username, :full_name, :hashed_password, :role, :status, :is_active, datetime('now'))
        """), {
            "email": "admin@example.com",
            "username": "admin",
            "full_name": "Admin User",
            "hashed_password": hashed_password,
            "role": "ADMIN",
            "status": "APPROVED",
            "is_active": True
        })
        
        db.commit()
        print("✅ Admin user created")
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Admin creation error: {e}")
        return False

def test_admin_login():
    """Test admin login"""
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post("http://localhost:8000/auth/login", json=login_data)
        print(f"Admin login response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful")
            return True
        else:
            print(f"❌ Admin login failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Admin login error: {e}")
        return False

if __name__ == "__main__":
    print("=== Login Test Suite ===")
    
    # Test database
    if not test_database_connection():
        print("❌ Database not working, stopping tests")
        exit(1)
    
    # Create admin user
    create_test_admin()
    
    # Test admin login
    test_admin_login()
    
    # Test user registration
    test_user_registration()
    
    # Test user login
    test_user_login()
    
    print("=== Test Complete ===")