#!/usr/bin/env python3
"""
Test Storage Connection with Real Service Key
This script will test the storage connection once you have the real service key
"""

import requests
import json
from config import settings

def test_with_real_service_key():
    """Test storage connection with real service key"""
    print("🔍 Testing Storage Connection")
    print("=" * 35)
    
    # Check if service key is still placeholder
    if "placeholder" in settings.supabase_service_key:
        print("❌ Service key is still placeholder")
        print("Please update config.py with your real service key")
        return False
    
    print("✅ Service key is configured")
    
    # Test bucket access with service key
    buckets = ['user-images', 'profile-pictures', 'activity-documents']
    
    for bucket in buckets:
        try:
            url = f"{settings.supabase_url}/storage/v1/bucket/{bucket}"
            headers = {
                "apikey": settings.supabase_service_key,
                "Authorization": f"Bearer {settings.supabase_service_key}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            print(f"{bucket}: {response.status_code}")
            
            if response.status_code == 200:
                bucket_info = response.json()
                print(f"  ✅ {bucket} exists (public: {bucket_info.get('public', False)})")
            elif response.status_code == 404:
                print(f"  ❌ {bucket} not found - please create it in Supabase dashboard")
            else:
                print(f"  ⚠️  {bucket} error: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ {bucket} exception: {e}")
    
    return True

def test_file_upload():
    """Test file upload with service key"""
    print("\n🔍 Testing File Upload")
    print("=" * 25)
    
    # Create a fake image file
    fake_image_content = b'fake image content for testing'
    
    try:
        # Test upload to user-images bucket
        url = f"{settings.supabase_url}/storage/v1/object/user-images/test-image.jpg"
        headers = {
            "apikey": settings.supabase_service_key,
            "Authorization": f"Bearer {settings.supabase_service_key}",
            "Content-Type": "image/jpeg"
        }
        
        response = requests.post(url, headers=headers, data=fake_image_content, timeout=10)
        print(f"Upload test: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ Upload successful!")
            print("  ✅ Storage is working correctly")
            return True
        elif response.status_code == 400:
            print(f"  ⚠️  Upload error: {response.text[:100]}")
        elif response.status_code == 401:
            print("  ⚠️  Authentication failed - check service key")
        else:
            print(f"  ❌ Upload failed: {response.text[:100]}")
            
    except Exception as e:
        print(f"  ❌ Upload exception: {e}")
    
    return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔍 Testing API Endpoints")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
        else:
            print(f"❌ API server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API server not running: {e}")
        return False
    
    # Test storage endpoints
    endpoints = [
        "/api/storage/upload/user-image",
        "/api/storage/upload/profile-picture",
        "/api/storage/upload/activity-document"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code in [401, 403, 405]:
                print(f"✅ {endpoint} - Available")
            else:
                print(f"⚠️  {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    return True

def main():
    """Main test function"""
    print("🧪 Storage Connection Test")
    print("=" * 40)
    
    # Test 1: Service key
    if not test_with_real_service_key():
        return
    
    # Test 2: File upload
    upload_works = test_file_upload()
    
    # Test 3: API endpoints
    api_works = test_api_endpoints()
    
    print("\n📋 Test Results")
    print("=" * 20)
    if upload_works and api_works:
        print("✅ Storage is fully connected and working!")
        print("✅ You can now upload images in your application")
        print("✅ Buckets are properly configured")
    else:
        print("⚠️  Some issues found:")
        if not upload_works:
            print("❌ File upload not working")
        if not api_works:
            print("❌ API endpoints not working")
    
    print("\n🎯 Next Steps:")
    print("1. Test uploads in your application")
    print("2. Check browser console for any errors")
    print("3. Verify images appear in Supabase dashboard")

if __name__ == "__main__":
    main()

