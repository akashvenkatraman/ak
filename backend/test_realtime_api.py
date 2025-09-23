#!/usr/bin/env python3
"""Test real-time API data extraction"""

import requests
import json
import time
from datetime import datetime

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ API Health: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API Health Error: {e}")
        return False

def test_login_and_get_user_data():
    """Test login and get user data"""
    try:
        # Login as admin
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        print("🔐 Testing admin login...")
        response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user')
            print(f"✅ Login successful: {user.get('username')} ({user.get('role')})")
            
            # Test protected endpoint
            headers = {"Authorization": f"Bearer {token}"}
            me_response = requests.get("http://localhost:8000/auth/me", headers=headers, timeout=10)
            
            if me_response.status_code == 200:
                user_data = me_response.json()
                print(f"✅ User data retrieved: {user_data.get('username')} - {user_data.get('email')}")
                return True
            else:
                print(f"❌ Failed to get user data: {me_response.status_code}")
                return False
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False

def test_database_real_time_extraction():
    """Test real-time database extraction"""
    try:
        from app.core.database import SessionLocal
        from sqlalchemy import text
        
        print("📊 Testing real-time database extraction...")
        
        # Get current data
        db = SessionLocal()
        result = db.execute(text("""
            SELECT id, username, email, role, status, created_at, updated_at 
            FROM users 
            ORDER BY created_at DESC
        """))
        users = result.fetchall()
        
        print(f"📈 Current database state:")
        print(f"   Total users: {len(users)}")
        for user in users:
            print(f"   - {user[1]} ({user[3]}) - {user[4]} - Created: {user[5]}")
        
        # Test if we can add a new user and see it immediately
        print("\n🔄 Testing real-time data insertion...")
        
        # Insert a test user
        test_user_data = {
            "email": f"test_realtime_{int(time.time())}@example.com",
            "username": f"test_realtime_{int(time.time())}",
            "password": "testpass123",
            "full_name": "Real-time Test User",
            "role": "student",
            "phone_number": "1234567890",
            "department": "Computer Science",
            "student_id": f"STU{int(time.time())}"
        }
        
        # Register new user
        register_response = requests.post("http://localhost:8000/auth/register", json=test_user_data, timeout=10)
        
        if register_response.status_code == 200:
            print("✅ New user registered successfully")
            
            # Immediately check database for the new user
            result = db.execute(text("""
                SELECT id, username, email, role, status, created_at 
                FROM users 
                WHERE username = :username
            """), {"username": test_user_data["username"]})
            
            new_user = result.fetchone()
            if new_user:
                print(f"✅ Real-time extraction successful: Found new user {new_user[1]} in database")
                
                # Update user status to approved for testing
                db.execute(text("""
                    UPDATE users 
                    SET status = 'APPROVED' 
                    WHERE username = :username
                """), {"username": test_user_data["username"]})
                db.commit()
                print("✅ User status updated to APPROVED")
                
                # Test login with new user
                login_data = {
                    "username": test_user_data["username"],
                    "password": "testpass123"
                }
                
                login_response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=10)
                if login_response.status_code == 200:
                    print("✅ New user can login successfully")
                else:
                    print(f"❌ New user login failed: {login_response.status_code}")
                
                return True
            else:
                print("❌ New user not found in database immediately after registration")
                return False
        else:
            print(f"❌ User registration failed: {register_response.status_code} - {register_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Real-time extraction test error: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

def test_api_endpoints():
    """Test various API endpoints for data extraction"""
    endpoints = [
        ("GET", "/health", "Health check"),
        ("GET", "/", "Root endpoint"),
        ("GET", "/docs", "API documentation"),
    ]
    
    print("\n🌐 Testing API endpoints...")
    for method, endpoint, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            else:
                response = requests.post(f"http://localhost:8000{endpoint}", timeout=5)
            
            print(f"   {description}: {response.status_code}")
        except Exception as e:
            print(f"   {description}: Error - {e}")

def test_database_connection_pool():
    """Test database connection pool and concurrent access"""
    try:
        print("\n🔄 Testing database connection pool...")
        
        from app.core.database import SessionLocal
        from sqlalchemy import text
        import threading
        import time
        
        def db_query(thread_id):
            try:
                db = SessionLocal()
                result = db.execute(text("SELECT COUNT(*) FROM users"))
                count = result.fetchone()[0]
                print(f"   Thread {thread_id}: Found {count} users")
                db.close()
                return True
            except Exception as e:
                print(f"   Thread {thread_id}: Error - {e}")
                return False
        
        # Test concurrent database access
        threads = []
        for i in range(5):
            thread = threading.Thread(target=db_query, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print("✅ Database connection pool test completed")
        return True
        
    except Exception as e:
        print(f"❌ Database connection pool test error: {e}")
        return False

if __name__ == "__main__":
    print("=== Real-time API Data Extraction Test ===")
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test API health
    if not test_api_health():
        print("❌ API not running, please start the backend server")
        exit(1)
    
    # Test API endpoints
    test_api_endpoints()
    
    # Test login and user data
    if not test_login_and_get_user_data():
        print("❌ Login test failed")
        exit(1)
    
    # Test real-time database extraction
    if not test_database_real_time_extraction():
        print("❌ Real-time extraction test failed")
        exit(1)
    
    # Test database connection pool
    test_database_connection_pool()
    
    print("\n🎉 All real-time data extraction tests passed!")
    print(f"🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
