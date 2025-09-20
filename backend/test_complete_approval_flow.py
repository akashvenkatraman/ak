#!/usr/bin/env python3
"""
Test complete approval flow
"""

import requests
import json
import time

def test_complete_approval_flow():
    """Test complete approval flow"""
    print("🚀 Testing Complete Approval Flow...")
    print("=" * 60)
    
    # Step 1: Register a new student
    print("📝 Step 1: Registering new student...")
    timestamp = int(time.time())
    student_data = {
        "full_name": "Test Student Approval",
        "email": f"approval{timestamp}@example.com",
        "username": f"approval{timestamp}",
        "password": "password123",
        "role": "student",
        "department": "engineering",
        "student_id": "99",
        "phone_number": "1234567890"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/register",
            json=student_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Student registration successful!")
            student_info = response.json()
            student_id = student_info['id']
            print(f"   Student ID: {student_id}")
            print(f"   Status: {student_info['status']}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # Step 2: Try to login as student (should fail - pending approval)
    print("\n📝 Step 2: Trying to login as student (should fail)...")
    login_data = {
        "username": student_data["username"],
        "password": student_data["password"]
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
            return False
    except Exception as e:
        print(f"❌ Error getting pending users: {e}")
        return False
    
    # Step 5: Approve the student
    print("\n📝 Step 5: Approving student...")
    try:
        approval_data = {
            "user_id": student_id,
            "status": "approved",
            "comments": "Approved by admin test"
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
            return False
    except Exception as e:
        print(f"❌ Approval error: {e}")
        return False
    
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
            print("🎉 Complete approval flow working perfectly!")
            return True
        else:
            print(f"❌ Student login still failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Student login error: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_approval_flow()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Complete approval flow test PASSED!")
        print("✅ Registration → Admin Approval → Login workflow is working!")
    else:
        print("❌ Complete approval flow test FAILED!")
        print("🔧 Check the error messages above for issues.")





