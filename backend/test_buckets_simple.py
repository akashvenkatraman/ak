#!/usr/bin/env python3
"""
Simple test to check if storage buckets are accessible
"""

import requests
from config import settings

def test_bucket_list():
    """Test if we can list buckets"""
    print("🧪 Testing Bucket Access")
    print("=" * 40)
    
    url = f"{settings.supabase_url}/storage/v1/bucket"
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            buckets = response.json()
            print(f"✅ Found {len(buckets)} buckets:")
            for bucket in buckets:
                print(f"   - {bucket.get('id', 'unknown')} (public: {bucket.get('public', False)})")
            return buckets
        else:
            print(f"❌ Error: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Exception: {e}")
        return []

def test_file_upload_simple():
    """Test simple file upload"""
    print("\n🔄 Testing File Upload")
    print("=" * 40)
    
    # Test with a simple image file
    test_content = b"fake image content for testing"
    test_path = "test_user/test_image.jpg"
    
    url = f"{settings.supabase_url}/storage/v1/object/user-images/{test_path}"
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "image/jpeg"
    }
    
    try:
        response = requests.post(url, headers=headers, data=test_content, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ File upload successful!")
            public_url = f"{settings.supabase_url}/storage/v1/object/public/user-images/{test_path}"
            print(f"Public URL: {public_url}")
            return True
        else:
            print("❌ File upload failed")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Simple Storage Test")
    print("=" * 50)
    
    # Test 1: List buckets
    buckets = test_bucket_list()
    
    # Test 2: Try file upload
    upload_success = test_file_upload_simple()
    
    # Summary
    print("\n📊 Test Results")
    print("=" * 30)
    print(f"Buckets found: {len(buckets)}")
    print(f"Upload test: {'✅ PASS' if upload_success else '❌ FAIL'}")
    
    if buckets and upload_success:
        print("\n🎉 Storage is working!")
        print("You can now use the storage API endpoints.")
    elif buckets and not upload_success:
        print("\n⚠️  Buckets exist but upload failed.")
        print("You may need to set buckets to 'Public' in Supabase dashboard.")
    else:
        print("\n❌ Storage not working.")
        print("Please check if buckets are created in Supabase dashboard.")

if __name__ == "__main__":
    main()
