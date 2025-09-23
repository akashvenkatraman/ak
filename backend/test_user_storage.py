#!/usr/bin/env python3
"""
Test script for user storage functionality
"""

import requests
import json
from setup_user_storage import SupabaseStorageSetup
from app.services.storage_service import storage_service

def test_storage_setup():
    """Test the storage setup"""
    print("🧪 Testing User Storage Setup")
    print("=" * 50)
    
    # Initialize setup
    setup = SupabaseStorageSetup()
    
    # Test connection
    print("1. Testing storage connection...")
    if setup.test_storage_connection():
        print("   ✅ Storage connection successful")
    else:
        print("   ❌ Storage connection failed")
        return False
    
    # List existing buckets
    print("\n2. Listing existing buckets...")
    buckets = setup.list_existing_buckets()
    if buckets:
        print("   ✅ Found existing buckets")
    else:
        print("   ⚠️  No buckets found")
    
    # Test storage service
    print("\n3. Testing storage service...")
    try:
        # Test with dummy data
        test_content = b"test image content"
        result = storage_service.upload_user_image(
            user_id=1,
            file_content=test_content,
            filename="test.jpg"
        )
        
        if result.get("success"):
            print("   ✅ Storage service working")
            print(f"   📁 File path: {result.get('file_path')}")
        else:
            print(f"   ❌ Storage service failed: {result.get('error')}")
    except Exception as e:
        print(f"   ❌ Storage service error: {e}")
    
    print("\n4. Testing API endpoints...")
    try:
        # Test if the API is running
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ API server is running")
        else:
            print("   ❌ API server not responding")
    except requests.exceptions.RequestException:
        print("   ⚠️  API server not running (start with: python main.py)")
    
    print("\n" + "=" * 50)
    print("🎯 Storage setup test completed!")
    print("\n📋 Next steps:")
    print("1. Update config.py with your Supabase service key")
    print("2. Run: python setup_user_storage.py")
    print("3. Apply RLS policies in Supabase SQL editor")
    print("4. Start the API server: python main.py")
    print("5. Test file uploads through the API")
    
    return True

if __name__ == "__main__":
    test_storage_setup()
