#!/usr/bin/env python3
"""
Test File Upload Script
Run this after getting a JWT token from login
"""

import requests
import json

# Replace with your actual JWT token from login
JWT_TOKEN = "YOUR_JWT_TOKEN_HERE"

def test_user_image_upload():
    """Test user image upload"""
    print("Testing User Image Upload")
    
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    
    # Create a fake image file
    files = {
        'file': ('test_image.jpg', b'fake image content for testing', 'image/jpeg')
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/storage/upload/user-image",
            headers=headers,
            files=files
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ User image upload successful!")
        else:
            print("❌ User image upload failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_profile_picture_upload():
    """Test profile picture upload"""
    print("
Testing Profile Picture Upload")
    
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    
    files = {
        'file': ('profile.jpg', b'fake profile picture content', 'image/jpeg')
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/storage/upload/profile-picture",
            headers=headers,
            files=files
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Profile picture upload successful!")
        else:
            print("❌ Profile picture upload failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_files():
    """Test getting user files"""
    print("
Testing Get User Files")
    
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    
    try:
        response = requests.get(
            "http://localhost:8000/api/storage/files/my-images",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Get files successful!")
        else:
            print("❌ Get files failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Storage Upload Test")
    print("=" * 20)
    print("1. Login to get JWT token")
    print("2. Replace JWT_TOKEN in this script")
    print("3. Run: python test_upload.py")
    print()
    
    if JWT_TOKEN == "YOUR_JWT_TOKEN_HERE":
        print("⚠️  Please set your JWT token first!")
    else:
        test_user_image_upload()
        test_profile_picture_upload()
        test_get_files()
