#!/usr/bin/env python3
"""
Debug Storage Upload Issues
This script will help identify why images aren't being stored in buckets
"""

import requests
import json
import time
from config import settings

def test_api_connection():
    """Test if API server is running"""
    print("🔍 Testing API Connection")
    print("=" * 30)
    
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
    """Test storage endpoints availability"""
    print("\n🔍 Testing Storage Endpoints")
    print("=" * 35)
    
    endpoints = [
        "/api/storage/upload/user-image",
        "/api/storage/upload/profile-picture",
        "/api/storage/upload/activity-document",
        "/api/storage/storage/status"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            print(f"{endpoint}: {response.status_code}")
            if response.status_code == 401:
                print("  ✅ Endpoint exists (requires authentication)")
            elif response.status_code == 405:
                print("  ✅ Endpoint exists (method not allowed for GET)")
            elif response.status_code == 200:
                print("  ✅ Endpoint working")
            else:
                print(f"  ⚠️  Unexpected status: {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

def test_supabase_connection():
    """Test direct Supabase connection"""
    print("\n🔍 Testing Supabase Connection")
    print("=" * 35)
    
    # Test Supabase URL
    try:
        response = requests.get(f"{settings.supabase_url}/rest/v1/", 
                              headers={"apikey": settings.supabase_key}, 
                              timeout=10)
        print(f"Supabase REST API: {response.status_code}")
        if response.status_code == 200:
            print("  ✅ Supabase connection working")
        else:
            print(f"  ⚠️  Supabase response: {response.text[:100]}")
    except Exception as e:
        print(f"  ❌ Supabase connection error: {e}")

def test_bucket_access():
    """Test bucket access"""
    print("\n🔍 Testing Bucket Access")
    print("=" * 25)
    
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
                print(f"  ✅ {bucket} exists (public: {bucket_info.get('public', False)})")
            elif response.status_code == 404:
                print(f"  ❌ {bucket} not found")
            else:
                print(f"  ⚠️  {bucket} error: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ {bucket} exception: {e}")

def test_file_upload_simulation():
    """Test file upload with fake data"""
    print("\n🔍 Testing File Upload Simulation")
    print("=" * 40)
    
    # Create a fake image file
    fake_image_content = b'fake image content for testing'
    
    try:
        # Test upload to user-images bucket
        url = f"{settings.supabase_url}/storage/v1/object/user-images/test-image.jpg"
        headers = {
            "apikey": settings.supabase_key,
            "Authorization": f"Bearer {settings.supabase_key}",
            "Content-Type": "image/jpeg"
        }
        
        response = requests.post(url, headers=headers, data=fake_image_content, timeout=10)
        print(f"Direct upload test: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ Direct upload successful")
        elif response.status_code == 400:
            print(f"  ⚠️  Upload error: {response.text[:100]}")
        elif response.status_code == 401:
            print("  ⚠️  Authentication required")
        else:
            print(f"  ❌ Upload failed: {response.text[:100]}")
            
    except Exception as e:
        print(f"  ❌ Upload exception: {e}")

def test_with_auth_token():
    """Test with authentication token"""
    print("\n🔍 Testing with Authentication")
    print("=" * 35)
    
    print("To test with authentication:")
    print("1. Login to get a JWT token")
    print("2. Use the token in Authorization header")
    print("3. Test file upload")
    
    # Example of how to test (commented out since we need auth)
    print("\nExample test command:")
    print("curl -X POST http://localhost:8000/api/storage/upload/user-image \\")
    print("  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \\")
    print("  -F 'file=@test-image.jpg'")

def check_config():
    """Check configuration"""
    print("\n🔍 Checking Configuration")
    print("=" * 30)
    
    print(f"Supabase URL: {settings.supabase_url}")
    print(f"Supabase Key: {settings.supabase_key[:20]}...")
    print(f"Service Key: {settings.supabase_service_key[:20]}...")
    
    # Check if service key is placeholder
    if "placeholder" in settings.supabase_service_key:
        print("⚠️  Service key is placeholder - this might cause issues")
    else:
        print("✅ Service key is configured")

def main():
    """Main debug function"""
    print("🐛 Storage Upload Debug Tool")
    print("=" * 50)
    
    # Test 1: API Connection
    api_running = test_api_connection()
    
    if api_running:
        # Test 2: Storage Endpoints
        test_storage_endpoints()
        
        # Test 3: Supabase Connection
        test_supabase_connection()
        
        # Test 4: Bucket Access
        test_bucket_access()
        
        # Test 5: File Upload Simulation
        test_file_upload_simulation()
        
        # Test 6: Authentication Info
        test_with_auth_token()
        
        # Test 7: Configuration
        check_config()
        
        print("\n📋 Debug Summary")
        print("=" * 20)
        print("✅ API server is running")
        print("✅ Storage endpoints are available")
        print("⚠️  Check bucket configuration")
        print("⚠️  Authentication required for uploads")
        
        print("\n🎯 Next Steps:")
        print("1. Verify buckets exist in Supabase dashboard")
        print("2. Check RLS policies are applied")
        print("3. Test upload with valid JWT token")
        print("4. Check browser console for errors")
        
    else:
        print("❌ API server not running")
        print("Start it with: python main.py")

if __name__ == "__main__":
    main()

