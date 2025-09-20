#!/usr/bin/env python3
"""
Test admin approval functionality
"""

import requests
import json
import time

def test_admin_login():
    """Test admin login and get token"""
    print("🔍 Testing Admin Login...")
    
    admin_data = {
        "username": "admin",
        "password": "admin123456"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/login",
            json=admin_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful!")
            print(f"Token: {data['access_token'][:50]}...")
            return data['access_token']
        else:
            print(f"❌ Admin login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Admin login error: {e}")
        return None

def test_pending_users(admin_token):
    """Test getting pending users"""
    print("\n🔍 Testing Pending Users API...")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    try:
        response = requests.get(
            "http://localhost:8000/admin/pending-users",
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} pending users")
            for user in users:
                print(f"   - ID: {user.get('id')}, Name: {user.get('full_name')}, Email: {user.get('email')}, Status: {user.get('status')}")
            return users
        else:
            print("❌ Failed to get pending users")
            return []
    except Exception as e:
        print(f"❌ Error getting pending users: {e}")
        return []

def test_all_users(admin_token):
    """Test getting all users"""
    print("\n🔍 Testing All Users API...")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    try:
        response = requests.get(
            "http://localhost:8000/admin/users",
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} total users")
            for user in users:
                print(f"   - ID: {user.get('id')}, Name: {user.get('full_name')}, Email: {user.get('email')}, Status: {user.get('status')}, Role: {user.get('role')}")
            return users
        else:
            print("❌ Failed to get all users")
            return []
    except Exception as e:
        print(f"❌ Error getting all users: {e}")
        return []

def test_approve_user(admin_token, user_id):
    """Test approving a user"""
    print(f"\n🔍 Testing User Approval for ID: {user_id}...")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    approval_data = {
        "user_id": user_id,
        "status": "approved",
        "comments": "Approved by admin test"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/admin/approve-user",
            json=approval_data,
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ User approval successful!")
            return True
        else:
            print("❌ User approval failed")
            return False
    except Exception as e:
        print(f"❌ Error approving user: {e}")
        return False

def test_database_directly():
    """Test database directly to see pending users"""
    print("\n🔍 Testing Database Directly...")
    
    try:
        from app.core.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            # Get all users
            result = conn.execute(text("SELECT id, full_name, email, role, status, created_at FROM users ORDER BY created_at DESC"))
            users = result.fetchall()
            
            print(f"✅ Found {len(users)} users in database:")
            for user in users:
                print(f"   - ID: {user.id}, Name: {user.full_name}, Email: {user.email}, Role: {user.role}, Status: {user.status}")
            
            # Get pending users specifically
            result = conn.execute(text("SELECT id, full_name, email, role, status FROM users WHERE status = 'pending'"))
            pending_users = result.fetchall()
            
            print(f"\n✅ Found {len(pending_users)} pending users:")
            for user in pending_users:
                print(f"   - ID: {user.id}, Name: {user.full_name}, Email: {user.email}, Role: {user.role}")
            
            return pending_users
    except Exception as e:
        print(f"❌ Database error: {e}")
        return []

if __name__ == "__main__":
    print("🚀 Testing Admin Approval System...")
    print("=" * 60)
    
    # Test admin login
    admin_token = test_admin_login()
    if not admin_token:
        print("❌ Cannot proceed without admin token")
        exit(1)
    
    # Test database directly
    pending_users_db = test_database_directly()
    
    # Test pending users API
    pending_users_api = test_pending_users(admin_token)
    
    # Test all users API
    all_users = test_all_users(admin_token)
    
    # If we have pending users, test approval
    if pending_users_api and len(pending_users_api) > 0:
        first_user = pending_users_api[0]
        test_approve_user(admin_token, first_user['id'])
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"Database Pending Users: {len(pending_users_db)}")
    print(f"API Pending Users: {len(pending_users_api)}")
    print(f"Total Users: {len(all_users)}")
    
    if len(pending_users_db) > 0 and len(pending_users_api) == 0:
        print("\n🔧 Issue Found: Database has pending users but API is not returning them!")
        print("This suggests an issue with the admin API endpoint.")
    elif len(pending_users_db) == 0:
        print("\nℹ️  No pending users in database. Try registering a new user first.")
    else:
        print("\n✅ Admin approval system is working correctly!")





