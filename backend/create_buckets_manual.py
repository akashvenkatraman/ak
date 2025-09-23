#!/usr/bin/env python3
"""
Manual Storage Bucket Creation Script
Creates storage buckets using the Supabase REST API
"""

import requests
import json
from config import settings

def create_bucket_manual(bucket_name: str, public: bool = True):
    """Create a storage bucket manually"""
    print(f"🪣 Creating bucket: {bucket_name}")
    
    # Supabase storage API endpoint
    url = f"{settings.supabase_url}/storage/v1/bucket"
    
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "id": bucket_name,
        "name": bucket_name,
        "public": public
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            print(f"   ✅ Successfully created bucket: {bucket_name}")
            return True
        elif response.status_code == 409:
            print(f"   ⚠️  Bucket already exists: {bucket_name}")
            return True
        else:
            print(f"   ❌ Failed to create bucket {bucket_name}")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error creating bucket {bucket_name}: {e}")
        return False

def list_buckets():
    """List existing buckets"""
    print("📦 Listing existing buckets...")
    
    url = f"{settings.supabase_url}/storage/v1/bucket"
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            buckets = response.json()
            print(f"   Found {len(buckets)} buckets:")
            for bucket in buckets:
                print(f"   - {bucket.get('id', 'unknown')} (public: {bucket.get('public', False)})")
            return buckets
        else:
            print(f"   ❌ Failed to list buckets: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ❌ Error listing buckets: {e}")
        return []

def main():
    """Main function to create storage buckets"""
    print("🚀 Creating User Storage Buckets")
    print("=" * 50)
    
    # Test connection first
    print("1. Testing connection...")
    buckets = list_buckets()
    print()
    
    # Create buckets
    print("2. Creating storage buckets...")
    bucket_configs = [
        {"name": "user-images", "public": True},
        {"name": "profile-pictures", "public": True},
        {"name": "activity-documents", "public": True}
    ]
    
    success_count = 0
    for config in bucket_configs:
        if create_bucket_manual(config["name"], config["public"]):
            success_count += 1
        print()
    
    # Final status
    print("3. Final status...")
    if success_count == len(bucket_configs):
        print("✅ All buckets created successfully!")
        print()
        print("📋 Next Steps:")
        print("1. Go to your Supabase dashboard")
        print("2. Navigate to Storage section")
        print("3. Verify the buckets are created")
        print("4. Set up RLS policies (see USER_STORAGE_SETUP.md)")
        print("5. Test file uploads")
    else:
        print(f"⚠️  {success_count}/{len(bucket_configs)} buckets created")
        print("Check the errors above and try again")
    
    # List final buckets
    print()
    print("4. Final bucket list:")
    list_buckets()

if __name__ == "__main__":
    main()
