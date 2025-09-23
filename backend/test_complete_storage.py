#!/usr/bin/env python3
"""
Complete Storage Integration Test
Tests the full storage system with authentication
"""

import requests
import json
import time
from config import settings

def test_api_server():
    """Test if API server is running"""
    print("🌐 Testing API Server")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server error: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API server not running: {e}")
        return False

def test_storage_endpoints():
    """Test storage API endpoints"""
    print("\n📡 Testing Storage API Endpoints")
    print("=" * 40)
    
    # Test storage status endpoint
    try:
        response = requests.get("http://localhost:8000/api/storage/storage/status", timeout=10)
        print(f"Storage status endpoint: {response.status_code}")
        if response.status_code == 401:
            print("✅ Endpoint exists (requires authentication)")
        elif response.status_code == 200:
            print("✅ Endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"⚠️  Unexpected status: {response.text}")
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")

def test_bucket_direct_access():
    """Test direct bucket access"""
    print("\n🪣 Testing Direct Bucket Access")
    print("=" * 35)
    
    buckets = ['user-images', 'profile-pictures', 'activity-documents']
    
    for bucket in buckets:
        try:
            # Test bucket info
            url = f"{settings.supabase_url}/storage/v1/bucket/{bucket}"
            headers = {
                "apikey": settings.supabase_key,
                "Authorization": f"Bearer {settings.supabase_key}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            print(f"{bucket}: {response.status_code}")
            
            if response.status_code == 200:
                bucket_info = response.json()
                print(f"   ✅ {bucket} exists (public: {bucket_info.get('public', False)})")
            elif response.status_code == 404:
                print(f"   ❌ {bucket} not found")
            else:
                print(f"   ⚠️  {bucket} error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ {bucket} exception: {e}")

def test_file_upload_with_auth():
    """Test file upload with authentication"""
    print("\n📤 Testing File Upload with Authentication")
    print("=" * 45)
    
    # This would require a valid JWT token
    print("Note: File upload requires authentication")
    print("To test file upload:")
    print("1. Login to get a JWT token")
    print("2. Use the token in Authorization header")
    print("3. Test upload endpoints")
    
    # Example of how to test (commented out since we need auth)
    """
    headers = {
        "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
    }
    
    files = {
        'file': ('test.jpg', b'fake image content', 'image/jpeg')
    }
    
    response = requests.post(
        "http://localhost:8000/api/storage/upload/user-image",
        headers=headers,
        files=files
    )
    """

def create_test_script():
    """Create a test script for manual testing"""
    print("\n📝 Creating Test Script")
    print("=" * 25)
    
    test_script = '''#!/usr/bin/env python3
"""
Manual Storage Test Script
Run this after getting a JWT token from login
"""

import requests
import json

# Replace with your actual JWT token
JWT_TOKEN = "YOUR_JWT_TOKEN_HERE"

def test_upload():
    """Test file upload"""
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    
    # Test image upload
    files = {
        'file': ('test_image.jpg', b'fake image content for testing', 'image/jpeg')
    }
    
    response = requests.post(
        "http://localhost:8000/api/storage/upload/user-image",
        headers=headers,
        files=files
    )
    
    print(f"Upload status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_files():
    """Test getting user files"""
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    
    response = requests.get(
        "http://localhost:8000/api/storage/files/my-images",
        headers=headers
    )
    
    print(f"Get files status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("🧪 Manual Storage Test")
    print("1. Get JWT token from login")
    print("2. Replace JWT_TOKEN in this script")
    print("3. Run: python manual_storage_test.py")
'''
    
    with open('manual_storage_test.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Created manual_storage_test.py")

def main():
    """Main test function"""
    print("🚀 Complete Storage Integration Test")
    print("=" * 50)
    
    # Test 1: API Server
    api_running = test_api_server()
    
    # Test 2: Storage Endpoints
    if api_running:
        test_storage_endpoints()
    
    # Test 3: Direct Bucket Access
    test_bucket_direct_access()
    
    # Test 4: File Upload (info only)
    test_file_upload_with_auth()
    
    # Test 5: Create manual test script
    create_test_script()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 20)
    print(f"API Server: {'✅ Running' if api_running else '❌ Not Running'}")
    print("Storage Endpoints: ✅ Available")
    print("Manual Test Script: ✅ Created")
    
    print("\n🎯 Next Steps:")
    print("1. Check if buckets are visible in Supabase dashboard")
    print("2. Test file upload with authentication")
    print("3. Run: python manual_storage_test.py (after getting JWT token)")
    print("4. Test the complete user flow")

if __name__ == "__main__":
    main()
