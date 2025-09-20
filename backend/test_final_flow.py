#!/usr/bin/env python3
"""
Final test of complete user flow
"""

import requests
import json
import time

def test_final_flow():
    """Test complete user flow with fresh data"""
    print("🚀 Testing Final Complete User Flow...")
    print("=" * 60)
    
    # Generate unique email
    timestamp = int(time.time())
    email = f"student{timestamp}@example.com"
    username = f"student{timestamp}"
    
    # Step 1: Register a new student
    print("📝 Step 1: Registering new student...")
    registration_data = {
        "full_name": "Akash V",
        "email": email,
        "username": username,
        "password": "password123",
        "role": "student",
        "department": "engineering",
        "student_id": "01",
        "phone_number": "09092266566"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/register", 
            json=registration_data, 
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Student registration successful!")
            student_data = response.json()
            print(f"   User ID: {student_data['id']}")
            print(f"   Status: {student_data['status']}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # Step 2: Try to login as student (should fail - pending approval)
    print("\n📝 Step 2: Trying to login as student (should fail)...")
    login_data = {
        "username": username,
        "password": "password123"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/login", 
            json=login_data, 
            timeout=10
        )
        
        if response.status_code == 403:
            print("✅ Login correctly blocked - account pending approval")
        else:
            print(f"⚠️  Unexpected response: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Step 3: Login as admin
    print("\n📝 Step 3: Logging in as admin...")
    admin_login = {
        "username": "admin",
        "password": "admin123456"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/login", 
            json=admin_login, 
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Admin login successful!")
            admin_data = response.json()
            admin_token = admin_data['access_token']
            print(f"   Token: {admin_token[:50]}...")
        else:
            print(f"❌ Admin login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Admin login error: {e}")
        return False
    
    # Step 4: Get pending users
    print("\n📝 Step 4: Getting pending users...")
    try:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            "http://localhost:8000/admin/pending-users", 
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            pending_users = response.json()
            print(f"✅ Found {len(pending_users)} pending users")
            for user in pending_users:
                print(f"   - {user['full_name']} ({user['email']}) - {user['status']}")
        else:
            print(f"❌ Failed to get pending users: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting pending users: {e}")
    
    # Step 5: Approve the student
    print("\n📝 Step 5: Approving student...")
    try:
        approval_data = {
            "user_id": student_data['id'],
            "status": "approved",
            "comments": "Approved by admin"
        }
        
        response = requests.post(
            "http://localhost:8000/admin/approve-user", 
            json=approval_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Student approved successfully!")
        else:
            print(f"❌ Approval failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Approval error: {e}")
    
    # Step 6: Try to login as student again (should succeed)
    print("\n📝 Step 6: Trying to login as student again...")
    try:
        response = requests.post(
            "http://localhost:8000/auth/login", 
            json=login_data, 
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Student login successful after approval!")
            student_login_data = response.json()
            print(f"   Student token: {student_login_data['access_token'][:50]}...")
            print("🎉 Complete flow working perfectly!")
        else:
            print(f"❌ Student login still failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Student login error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Final flow test completed!")
    return True

if __name__ == "__main__":
    test_final_flow()





