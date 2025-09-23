#!/usr/bin/env python3
"""Test frontend API connection and data display"""

import requests
import json
import time

def test_frontend_api_connection():
    """Test if frontend can connect to API"""
    try:
        print("🌐 Testing frontend API connection...")
        
        # Test CORS preflight
        response = requests.options("http://localhost:8000/auth/login", 
                                  headers={
                                      "Origin": "http://localhost:3000",
                                      "Access-Control-Request-Method": "POST",
                                      "Access-Control-Request-Headers": "Content-Type"
                                  })
        print(f"   CORS preflight: {response.status_code}")
        
        # Test login endpoint
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post("http://localhost:8000/auth/login", 
                               json=login_data,
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful: {data.get('user', {}).get('username')}")
            
            # Test protected endpoint
            token = data.get('access_token')
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            me_response = requests.get("http://localhost:8000/auth/me", headers=headers, timeout=10)
            if me_response.status_code == 200:
                user_data = me_response.json()
                print(f"   ✅ User data retrieved: {user_data.get('username')} - {user_data.get('email')}")
                print(f"   ✅ User role: {user_data.get('role')}")
                print(f"   ✅ User status: {user_data.get('status')}")
                return True
            else:
                print(f"   ❌ Failed to get user data: {me_response.status_code}")
                return False
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Frontend API connection error: {e}")
        return False

def test_data_consistency():
    """Test data consistency between database and API"""
    try:
        print("\n📊 Testing data consistency...")
        
        from app.core.database import SessionLocal
        from sqlalchemy import text
        
        # Get data from database
        db = SessionLocal()
        result = db.execute(text("""
            SELECT id, username, email, role, status, created_at 
            FROM users 
            ORDER BY created_at DESC
        """))
        db_users = result.fetchall()
        db.close()
        
        print(f"   Database users: {len(db_users)}")
        for user in db_users:
            print(f"     - {user[1]} ({user[3]}) - {user[4]}")
        
        # Get data from API
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test if we can get all users (admin endpoint)
            try:
                users_response = requests.get("http://localhost:8000/admin/users", headers=headers, timeout=10)
                if users_response.status_code == 200:
                    api_users = users_response.json()
                    print(f"   API users: {len(api_users)}")
                    for user in api_users:
                        print(f"     - {user.get('username')} ({user.get('role')}) - {user.get('status')}")
                    
                    # Compare counts
                    if len(db_users) == len(api_users):
                        print("   ✅ Data consistency: Database and API user counts match")
                        return True
                    else:
                        print(f"   ❌ Data inconsistency: DB has {len(db_users)} users, API has {len(api_users)} users")
                        return False
                else:
                    print(f"   ❌ Failed to get users from API: {users_response.status_code}")
                    return False
            except Exception as e:
                print(f"   ❌ API users endpoint error: {e}")
                return False
        else:
            print("   ❌ Login failed for data consistency test")
            return False
            
    except Exception as e:
        print(f"   ❌ Data consistency test error: {e}")
        return False

def test_real_time_updates():
    """Test real-time data updates"""
    try:
        print("\n🔄 Testing real-time updates...")
        
        # Login as admin
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get initial user count
            users_response = requests.get("http://localhost:8000/admin/users", headers=headers, timeout=10)
            if users_response.status_code == 200:
                initial_users = users_response.json()
                initial_count = len(initial_users)
                print(f"   Initial user count: {initial_count}")
                
                # Add a new user
                new_user_data = {
                    "email": f"realtime_test_{int(time.time())}@example.com",
                    "username": f"realtime_test_{int(time.time())}",
                    "password": "testpass123",
                    "full_name": "Real-time Test User",
                    "role": "student",
                    "phone_number": "1234567890",
                    "department": "Computer Science",
                    "student_id": f"STU{int(time.time())}"
                }
                
                register_response = requests.post("http://localhost:8000/auth/register", json=new_user_data, timeout=10)
                if register_response.status_code == 200:
                    print("   ✅ New user registered")
                    
                    # Wait a moment for database update
                    time.sleep(1)
                    
                    # Check if new user appears in API
                    users_response = requests.get("http://localhost:8000/admin/users", headers=headers, timeout=10)
                    if users_response.status_code == 200:
                        updated_users = users_response.json()
                        updated_count = len(updated_users)
                        print(f"   Updated user count: {updated_count}")
                        
                        if updated_count > initial_count:
                            print("   ✅ Real-time update successful: New user visible in API")
                            return True
                        else:
                            print("   ❌ Real-time update failed: New user not visible in API")
                            return False
                    else:
                        print("   ❌ Failed to get updated users from API")
                        return False
                else:
                    print(f"   ❌ User registration failed: {register_response.status_code}")
                    return False
            else:
                print("   ❌ Failed to get initial users from API")
                return False
        else:
            print("   ❌ Login failed for real-time update test")
            return False
            
    except Exception as e:
        print(f"   ❌ Real-time update test error: {e}")
        return False

if __name__ == "__main__":
    print("=== Frontend API Connection & Real-time Data Test ===")
    print(f"🕐 Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test frontend API connection
    if not test_frontend_api_connection():
        print("❌ Frontend API connection test failed")
        exit(1)
    
    # Test data consistency
    if not test_data_consistency():
        print("❌ Data consistency test failed")
        exit(1)
    
    # Test real-time updates
    if not test_real_time_updates():
        print("❌ Real-time updates test failed")
        exit(1)
    
    print("\n🎉 All frontend API connection and real-time data tests passed!")
    print("✅ Frontend can connect to API")
    print("✅ Data is consistent between database and API")
    print("✅ Real-time data extraction is working")
    print(f"🕐 Test completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
