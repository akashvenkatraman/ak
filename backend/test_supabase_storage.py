#!/usr/bin/env python3
"""Test Supabase storage setup and file upload functionality"""

import requests
import json
import os
from supabase_fast_client import supabase_fast
from file_upload_service import file_upload_service
from create_file_storage_table import create_file_storage_table

def test_supabase_connection():
    """Test Supabase connection"""
    print("🔗 Testing Supabase connection...")
    
    if supabase_fast.test_connection():
        print("✅ Supabase connection successful")
        return True
    else:
        print("❌ Supabase connection failed")
        return False

def test_storage_buckets():
    """Test storage bucket creation and listing"""
    print("\n🪣 Testing storage buckets...")
    
    # Setup storage buckets
    success = supabase_fast.setup_storage_buckets()
    if success:
        print("✅ Storage buckets setup completed")
    else:
        print("❌ Storage buckets setup failed")
        return False
    
    # List buckets
    buckets = supabase_fast.list_buckets()
    print(f"📦 Available buckets: {len(buckets)}")
    for bucket in buckets:
        print(f"  - {bucket.get('name', 'Unknown')} (Public: {bucket.get('public', False)})")
    
    return True

def test_file_upload():
    """Test file upload functionality"""
    print("\n📁 Testing file upload...")
    
    # Create a test file
    test_content = b"This is a test certificate file content"
    test_filename = "test_certificate.pdf"
    
    # Test certificate upload
    result = file_upload_service.upload_certificate(
        file_content=test_content,
        filename=test_filename,
        user_id=1,  # Assuming user ID 1 exists
        activity_id=None
    )
    
    if result["success"]:
        print("✅ Certificate upload successful")
        print(f"  - File ID: {result['file_id']}")
        print(f"  - Supabase URL: {result['supabase_url']}")
        print(f"  - Local Path: {result['local_path']}")
        return True
    else:
        print(f"❌ Certificate upload failed: {result.get('error', 'Unknown error')}")
        return False

def test_file_retrieval():
    """Test file retrieval"""
    print("\n🔍 Testing file retrieval...")
    
    # Get user files
    files = file_upload_service.get_user_files(user_id=1)
    print(f"📁 Found {len(files)} files for user 1")
    
    for file_info in files:
        print(f"  - {file_info['original_filename']} ({file_info['file_type']})")
        print(f"    Size: {file_info['file_size']} bytes")
        print(f"    URL: {file_info['supabase_url']}")
    
    return len(files) > 0

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test file upload endpoint (requires authentication)
    print("⚠️  File upload endpoints require authentication - skipping for now")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Supabase storage tests...\n")
    
    # Create file storage table
    print("📊 Creating file storage table...")
    if create_file_storage_table():
        print("✅ File storage table created")
    else:
        print("❌ Failed to create file storage table")
        return
    
    # Test Supabase connection
    if not test_supabase_connection():
        print("\n❌ Supabase connection failed - cannot proceed with storage tests")
        return
    
    # Test storage buckets
    if not test_storage_buckets():
        print("\n❌ Storage bucket tests failed")
        return
    
    # Test file upload
    if not test_file_upload():
        print("\n❌ File upload tests failed")
        return
    
    # Test file retrieval
    if not test_file_retrieval():
        print("\n❌ File retrieval tests failed")
        return
    
    # Test API endpoints
    if not test_api_endpoints():
        print("\n❌ API endpoint tests failed")
        return
    
    print("\n🎉 All Supabase storage tests completed successfully!")
    print("\n📋 Summary:")
    print("  ✅ Supabase connection established")
    print("  ✅ Storage buckets created")
    print("  ✅ File upload functionality working")
    print("  ✅ File retrieval functionality working")
    print("  ✅ API endpoints accessible")
    print("\n🔗 Your Supabase storage is ready for certificate uploads!")

if __name__ == "__main__":
    main()
