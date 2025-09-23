#!/usr/bin/env python3
"""
Check users in Supabase
"""

import requests
from config import settings

def check_supabase_users():
    print("🔍 Checking users in Supabase...")
    
    # Use Supabase REST API directly
    url = f"{settings.supabase_url}/rest/v1/users"
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"📡 Supabase response status: {response.status_code}")
        print(f"📡 Supabase response: {response.text}")
        
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    check_supabase_users()
