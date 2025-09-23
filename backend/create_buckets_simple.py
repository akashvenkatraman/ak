#!/usr/bin/env python3
"""
Simple script to create storage buckets using the correct API approach
"""

import requests
import json
from config import settings

def create_bucket_simple(bucket_name: str):
    """Create a storage bucket using the simple approach"""
    print(f"🪣 Creating bucket: {bucket_name}")
    
    # Use the storage API with proper headers
    url = f"{settings.supabase_url}/storage/v1/bucket"
    
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json"
    }
    
    # Simple bucket data
    data = {
        "id": bucket_name,
        "name": bucket_name,
        "public": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print(f"   ✅ Successfully created: {bucket_name}")
            return True
        elif response.status_code == 409:
            print(f"   ⚠️  Already exists: {bucket_name}")
            return True
        else:
            print(f"   ❌ Failed to create: {bucket_name}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Create all required buckets"""
    print("🚀 Creating Storage Buckets")
    print("=" * 50)
    
    buckets = [
        "user-images",
        "profile-pictures", 
        "activity-documents"
    ]
    
    success_count = 0
    for bucket in buckets:
        if create_bucket_simple(bucket):
            success_count += 1
        print()
    
    print(f"📊 Created {success_count}/{len(buckets)} buckets")
    
    if success_count == len(buckets):
        print("✅ All buckets created successfully!")
        print("\n📋 Next Steps:")
        print("1. Go to Supabase dashboard → Storage")
        print("2. Verify the buckets are visible")
        print("3. Run: python test_storage_setup.py")
    else:
        print("⚠️  Some buckets failed to create")
        print("You may need to create them manually in the Supabase dashboard")

if __name__ == "__main__":
    main()
