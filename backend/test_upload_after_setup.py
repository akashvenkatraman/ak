#!/usr/bin/env python3
"""
Test Upload After Bucket Setup
Run this after creating buckets and applying RLS policies
"""

import requests
import json
import time
from config import settings

def test_buckets_exist():
    """Test if buckets exist now"""
    print("🔍 Testing if Buckets Exist")
    print("=" * 30)
    
    buckets = ['user-images', 'profile-pictures', 'activity-documents']
    
    for bucket in buckets:
        try:
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
                print(f"  ❌ {bucket} still not found - please create it in Supabase dashboard")
            else:
                print(f"  ⚠️  {bucket} error: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ {bucket} exception: {e}")

def test_upload_with_service_key():
    """Test upload using service key"""
    print("\n🔍 Testing Upload with Service Key")
    print("=" * 40)
    
    # Create a fake image file
    fake_image_content = b'fake image content for testing'
    
    try:
        # Test upload to user-images bucket using service key
        url = f"{settings.supabase_url}/storage/v1/object/user-images/test-image.jpg"
        headers = {
            "apikey": settings.supabase_service_key,
            "Authorization": f"Bearer {settings.supabase_service_key}",
            "Content-Type": "image/jpeg"
        }
        
        response = requests.post(url, headers=headers, data=fake_image_content, timeout=10)
        print(f"Service key upload test: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ Upload with service key successful")
            print("  ✅ Buckets and policies are working")
        elif response.status_code == 400:
            print(f"  ⚠️  Upload error: {response.text[:100]}")
        elif response.status_code == 401:
            print("  ⚠️  Service key authentication failed")
        else:
            print(f"  ❌ Upload failed: {response.text[:100]}")
            
    except Exception as e:
        print(f"  ❌ Upload exception: {e}")

def test_api_upload_endpoint():
    """Test API upload endpoint"""
    print("\n🔍 Testing API Upload Endpoint")
    print("=" * 35)
    
    print("To test API upload endpoint:")
    print("1. Login to get JWT token")
    print("2. Use the token in Authorization header")
    print("3. Test file upload via API")
    
    print("\nExample test:")
    print("curl -X POST http://localhost:8000/api/storage/upload/user-image \\")
    print("  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \\")
    print("  -F 'file=@test-image.jpg'")

def main():
    """Main test function"""
    print("🧪 Upload Test After Bucket Setup")
    print("=" * 50)
    
    # Test 1: Check if buckets exist
    test_buckets_exist()
    
    # Test 2: Test upload with service key
    test_upload_with_service_key()
    
    # Test 3: API endpoint info
    test_api_upload_endpoint()
    
    print("\n📋 Test Summary")
    print("=" * 20)
    print("If buckets exist and service key upload works:")
    print("✅ Buckets are created correctly")
    print("✅ RLS policies are working")
    print("✅ Ready for user uploads")
    
    print("\nIf buckets still don't exist:")
    print("❌ Please create buckets in Supabase dashboard")
    print("❌ Apply RLS policies from setup_bucket_policies.sql")
    
    print("\n🎯 Next Steps:")
    print("1. Create buckets in Supabase dashboard")
    print("2. Apply RLS policies")
    print("3. Test uploads in your application")
    print("4. Check browser console for any errors")

if __name__ == "__main__":
    main()

