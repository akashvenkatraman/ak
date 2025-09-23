#!/usr/bin/env python3
"""
Get Real Supabase Service Key
This script will help you get your actual service key from Supabase
"""

def main():
    print("🔑 Getting Your Supabase Service Key")
    print("=" * 50)
    
    print("To get your service key:")
    print("1. Go to: https://supabase.com/dashboard")
    print("2. Select your project: ieugtoltckngbxreohcv")
    print("3. Click 'Settings' in the left sidebar")
    print("4. Click 'API' in the settings menu")
    print("5. Copy the 'service_role' key (NOT the anon key)")
    print("6. It should start with: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    print()
    print("⚠️  IMPORTANT:")
    print("- Use the 'service_role' key, NOT the 'anon' key")
    print("- The service_role key has more permissions")
    print("- Keep it secure and don't share it publicly")
    print()
    print("Once you have the service key:")
    print("1. Replace the placeholder in config.py")
    print("2. Restart the backend server")
    print("3. Test the storage connection")

if __name__ == "__main__":
    main()

