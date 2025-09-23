#!/usr/bin/env python3
"""
Verify Storage Buckets in Supabase
"""

import requests
from config import settings

def check_buckets():
    """Check if buckets exist in Supabase"""
    print("Checking Storage Buckets")
    print("=" * 30)
    
    # List all buckets
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
            print(f"Found {len(buckets)} buckets:")
            
            if buckets:
                for bucket in buckets:
                    print(f"  - {bucket.get('id', 'unknown')} (public: {bucket.get('public', False)})")
            else:
                print("  No buckets found!")
                print("\nThis means the buckets haven't been created yet.")
                print("Please go to your Supabase dashboard and create them manually.")
                
            return buckets
        else:
            print(f"Error: {response.text}")
            return []
    except Exception as e:
        print(f"Exception: {e}")
        return []

def check_individual_buckets():
    """Check individual buckets"""
    print("\nChecking Individual Buckets")
    print("=" * 30)
    
    bucket_names = ['user-images', 'profile-pictures', 'activity-documents']
    
    for bucket_name in bucket_names:
        url = f"{settings.supabase_url}/storage/v1/bucket/{bucket_name}"
        headers = {
            "apikey": settings.supabase_key,
            "Authorization": f"Bearer {settings.supabase_key}"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"  {bucket_name}: EXISTS")
            elif response.status_code == 404:
                print(f"  {bucket_name}: NOT FOUND")
            else:
                print(f"  {bucket_name}: ERROR ({response.status_code})")
        except Exception as e:
            print(f"  {bucket_name}: EXCEPTION ({e})")

def main():
    """Main function"""
    print("Supabase Storage Bucket Verification")
    print("=" * 40)
    
    # Check all buckets
    buckets = check_buckets()
    
    # Check individual buckets
    check_individual_buckets()
    
    # Summary
    print("\nSummary")
    print("=" * 10)
    if buckets:
        print("Buckets are created and accessible!")
        print("You can now test file uploads.")
    else:
        print("Buckets are NOT created yet.")
        print("\nTo create buckets:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Select your project: ieugtoltckngbxreohcv")
        print("3. Click 'Storage' in the left sidebar")
        print("4. Click 'New bucket' and create:")
        print("   - user-images (public: true)")
        print("   - profile-pictures (public: true)")
        print("   - activity-documents (public: true)")

if __name__ == "__main__":
    main()

