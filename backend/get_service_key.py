#!/usr/bin/env python3
"""
Script to help you get your Supabase service key
"""

print("🔑 Getting Supabase Service Key")
print("=" * 50)
print()
print("To get your service key:")
print("1. Go to: https://supabase.com/dashboard")
print("2. Select your project: ieugtoltckngbxreohcv")
print("3. Go to Settings → API")
print("4. Copy the 'service_role' key (NOT the anon key)")
print("5. The service key should start with 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'")
print("6. It should contain 'service_role' in the payload")
print()
print("⚠️  IMPORTANT: The service key is different from your anon key!")
print("   - Anon key (what you have): Contains 'anon' role")
print("   - Service key (what you need): Contains 'service_role' role")
print()
print("Once you have the service key, update config.py with it.")
print("Then run: python setup_user_storage.py")
