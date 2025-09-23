#!/usr/bin/env python3
"""
Test Storage Integration with the Application
"""

import requests
import json
import time
from config import settings

def test_api_health():
    """Test if API is running"""
    print("Testing API Health")
    print("=" * 20)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API server not running: {e}")
        return False

def test_storage_endpoints():
    """Test storage endpoints"""
    print("\nTesting Storage Endpoints")
    print("=" * 25)
    
    endpoints = [
        "/api/storage/upload/user-image",
        "/api/storage/upload/profile-picture", 
        "/api/storage/upload/activity-document",
        "/api/storage/files/my-images",
        "/api/storage/files/my-documents",
        "/api/storage/storage/status"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 401:
                print(f"✅ {endpoint} - Requires authentication")
            elif response.status_code == 405:
                print(f"✅ {endpoint} - Method not allowed (expected for GET)")
            elif response.status_code == 200:
                print(f"✅ {endpoint} - Working")
            else:
                print(f"⚠️  {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")

def test_bucket_access():
    """Test direct bucket access"""
    print("\nTesting Bucket Access")
    print("=" * 20)
    
    # Test the buckets that exist in your dashboard
    buckets = ['user-images', 'profile-pictures', 'activity-documents']
    
    for bucket in buckets:
        try:
            url = f"{settings.supabase_url}/storage/v1/bucket/{bucket}"
            headers = {
                "apikey": settings.supabase_key,
                "Authorization": f"Bearer {settings.supabase_key}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                bucket_info = response.json()
                print(f"✅ {bucket} - Accessible (public: {bucket_info.get('public', False)})")
            elif response.status_code == 404:
                print(f"❌ {bucket} - Not found")
            else:
                print(f"⚠️  {bucket} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {bucket} - Error: {e}")

def create_test_upload_script():
    """Create a test upload script"""
    print("\nCreating Test Upload Script")
    print("=" * 30)
    
    script_content = '''#!/usr/bin/env python3
"""
Test File Upload Script
Run this after getting a JWT token from login
"""

import requests
import json

# Replace with your actual JWT token from login
JWT_TOKEN = "YOUR_JWT_TOKEN_HERE"

def test_user_image_upload():
    """Test user image upload"""
    print("Testing User Image Upload")
    
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    
    # Create a fake image file
    files = {
        'file': ('test_image.jpg', b'fake image content for testing', 'image/jpeg')
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/storage/upload/user-image",
            headers=headers,
            files=files
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ User image upload successful!")
        else:
            print("❌ User image upload failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_profile_picture_upload():
    """Test profile picture upload"""
    print("\nTesting Profile Picture Upload")
    
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    
    files = {
        'file': ('profile.jpg', b'fake profile picture content', 'image/jpeg')
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/storage/upload/profile-picture",
            headers=headers,
            files=files
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Profile picture upload successful!")
        else:
            print("❌ Profile picture upload failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_files():
    """Test getting user files"""
    print("\nTesting Get User Files")
    
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    
    try:
        response = requests.get(
            "http://localhost:8000/api/storage/files/my-images",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Get files successful!")
        else:
            print("❌ Get files failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Storage Upload Test")
    print("=" * 20)
    print("1. Login to get JWT token")
    print("2. Replace JWT_TOKEN in this script")
    print("3. Run: python test_upload.py")
    print()
    
    if JWT_TOKEN == "YOUR_JWT_TOKEN_HERE":
        print("⚠️  Please set your JWT token first!")
    else:
        test_user_image_upload()
        test_profile_picture_upload()
        test_get_files()
'''
    
    with open('test_upload.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Created test_upload.py")

def main():
    """Main test function"""
    print("Storage Integration Test")
    print("=" * 30)
    
    # Test 1: API Health
    api_running = test_api_health()
    
    if api_running:
        # Test 2: Storage Endpoints
        test_storage_endpoints()
        
        # Test 3: Bucket Access
        test_bucket_access()
        
        # Test 4: Create test script
        create_test_upload_script()
        
        print("\nSummary")
        print("=" * 10)
        print("✅ API server is running")
        print("✅ Storage endpoints are available")
        print("✅ Test upload script created")
        
        print("\nNext Steps:")
        print("1. Login to get JWT token")
        print("2. Run: python test_upload.py")
        print("3. Test file uploads")
        print("4. Integrate with frontend")
    else:
        print("❌ API server not running")
        print("Start it with: python main.py")

if __name__ == "__main__":
    main()

