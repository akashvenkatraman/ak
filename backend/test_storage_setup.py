#!/usr/bin/env python3
"""
Test script to verify storage buckets and functionality
"""

import requests
import json
from config import settings

def test_bucket_access():
    """Test if we can access the storage buckets"""
    print("🧪 Testing Storage Bucket Access")
    print("=" * 50)
    
    # Test connection to Supabase storage
    url = f"{settings.supabase_url}/storage/v1/bucket"
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            buckets = response.json()
            print(f"✅ Successfully connected to Supabase storage")
            print(f"📦 Found {len(buckets)} buckets:")
            
            bucket_names = []
            for bucket in buckets:
                name = bucket.get('id', 'unknown')
                public = bucket.get('public', False)
                print(f"   - {name} (public: {public})")
                bucket_names.append(name)
            
            # Check if our required buckets exist
            required_buckets = ['user-images', 'profile-pictures', 'activity-documents']
            missing_buckets = [b for b in required_buckets if b not in bucket_names]
            
            if not missing_buckets:
                print(f"\n✅ All required buckets are present!")
                return True
            else:
                print(f"\n❌ Missing buckets: {missing_buckets}")
                return False
                
        else:
            print(f"❌ Failed to connect to storage: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to storage: {e}")
        return False

def test_file_upload():
    """Test file upload functionality"""
    print("\n🔄 Testing File Upload Functionality")
    print("=" * 50)
    
    # Test with a simple text file
    test_content = b"test file content for storage testing"
    test_filename = "test_file.txt"
    
    # Try to upload to user-images bucket
    upload_url = f"{settings.supabase_url}/storage/v1/object/user-images/test_user/test_{test_filename}"
    
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "text/plain"
    }
    
    try:
        response = requests.post(
            upload_url,
            headers=headers,
            data=test_content,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ File upload test successful!")
            print(f"📁 File uploaded to: user-images/test_user/test_{test_filename}")
            
            # Get the public URL
            public_url = f"{settings.supabase_url}/storage/v1/object/public/user-images/test_user/test_{test_filename}"
            print(f"🔗 Public URL: {public_url}")
            
            return True
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ File upload error: {e}")
        return False

def test_storage_api():
    """Test the storage API endpoints"""
    print("\n🌐 Testing Storage API Endpoints")
    print("=" * 50)
    
    # Test if the API server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            
            # Test storage status endpoint (this will require authentication)
            print("📊 Testing storage endpoints...")
            print("   Note: Storage endpoints require authentication")
            print("   Start your API server with: python main.py")
            print("   Then test with a valid JWT token")
            
            return True
        else:
            print("❌ API server not responding")
            return False
    except requests.exceptions.RequestException:
        print("⚠️  API server not running")
        print("   Start it with: python main.py")
        return False

def main():
    """Main test function"""
    print("🚀 Storage Setup Verification")
    print("=" * 50)
    
    # Test 1: Bucket access
    bucket_test = test_bucket_access()
    
    # Test 2: File upload
    upload_test = test_file_upload()
    
    # Test 3: API endpoints
    api_test = test_storage_api()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"Bucket Access: {'✅ PASS' if bucket_test else '❌ FAIL'}")
    print(f"File Upload: {'✅ PASS' if upload_test else '❌ FAIL'}")
    print(f"API Server: {'✅ PASS' if api_test else '⚠️  NOT RUNNING'}")
    
    if bucket_test and upload_test:
        print("\n🎉 Storage setup is working correctly!")
        print("\n📋 Next Steps:")
        print("1. Start your API server: python main.py")
        print("2. Test file uploads through the API endpoints")
        print("3. Integrate with your frontend application")
        print("4. Test user authentication and file access")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        if not bucket_test:
            print("   - Verify buckets are created in Supabase dashboard")
        if not upload_test:
            print("   - Check RLS policies are applied correctly")

if __name__ == "__main__":
    main()
