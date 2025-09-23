#!/usr/bin/env python3
"""Fast Supabase client using REST API for optimal performance"""

import requests
import json
import time
from typing import Dict, List, Optional, Any, BinaryIO
from config import settings
import base64
import mimetypes

class SupabaseFastClient:
    def __init__(self):
        self.url = settings.supabase_url
        self.key = settings.supabase_key
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        self.storage_headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
        }
        self.connection_pool = requests.Session()
        self.connection_pool.headers.update(self.headers)
    
    def test_connection(self) -> bool:
        """Test Supabase connection with timeout"""
        try:
            response = self.connection_pool.get(
                f"{self.url}/rest/v1/users?select=count",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Supabase connection test failed: {e}")
            return False
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users with fast connection"""
        try:
            response = self.connection_pool.get(
                f"{self.url}/rest/v1/users?select=*",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create user with fast connection"""
        try:
            response = self.connection_pool.post(
                f"{self.url}/rest/v1/users",
                json=user_data,
                timeout=10
            )
            if response.status_code == 201:
                return response.json()[0] if response.json() else None
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user with fast connection"""
        try:
            response = self.connection_pool.patch(
                f"{self.url}/rest/v1/users?id=eq.{user_id}",
                json=user_data,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()[0] if response.json() else None
            return None
        except Exception as e:
            print(f"Error updating user: {e}")
            return None
    
    # Storage methods for certificates
    def create_bucket(self, bucket_name: str, public: bool = True) -> bool:
        """Create a storage bucket for certificates"""
        try:
            bucket_data = {
                "id": bucket_name,
                "name": bucket_name,
                "public": public
            }
            
            response = self.connection_pool.post(
                f"{self.url}/storage/v1/bucket",
                json=bucket_data,
                headers=self.storage_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Created bucket: {bucket_name}")
                return True
            else:
                print(f"❌ Failed to create bucket: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error creating bucket: {e}")
            return False
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """List all storage buckets"""
        try:
            response = self.connection_pool.get(
                f"{self.url}/storage/v1/bucket",
                headers=self.storage_headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error listing buckets: {e}")
            return []
    
    def upload_certificate(self, file_path: str, file_content: bytes, 
                          user_id: int, activity_id: Optional[int] = None) -> Optional[str]:
        """Upload certificate to Supabase storage"""
        try:
            # Generate unique filename
            import uuid
            file_extension = file_path.split('.')[-1] if '.' in file_path else 'pdf'
            unique_filename = f"{user_id}_{activity_id or 'general'}_{uuid.uuid4().hex}.{file_extension}"
            
            # Upload to certificates bucket
            bucket_name = "certificates"
            upload_path = f"certificates/{unique_filename}"
            
            # Set content type
            content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            
            response = self.connection_pool.post(
                f"{self.url}/storage/v1/object/{bucket_name}/{upload_path}",
                data=file_content,
                headers={
                    **self.storage_headers,
                    "Content-Type": content_type
                },
                timeout=30
            )
            
            if response.status_code == 200:
                # Return public URL
                public_url = f"{self.url}/storage/v1/object/public/{bucket_name}/{upload_path}"
                print(f"✅ Certificate uploaded: {public_url}")
                return public_url
            else:
                print(f"❌ Upload failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error uploading certificate: {e}")
            return None
    
    def upload_profile_picture(self, file_path: str, file_content: bytes, user_id: int) -> Optional[str]:
        """Upload profile picture to Supabase storage"""
        try:
            # Generate unique filename
            import uuid
            file_extension = file_path.split('.')[-1] if '.' in file_path else 'jpg'
            unique_filename = f"{user_id}_{uuid.uuid4().hex}.{file_extension}"
            
            # Upload to profile-pictures bucket
            bucket_name = "profile-pictures"
            upload_path = f"profile-pictures/{unique_filename}"
            
            # Set content type
            content_type = mimetypes.guess_type(file_path)[0] or 'image/jpeg'
            
            response = self.connection_pool.post(
                f"{self.url}/storage/v1/object/{bucket_name}/{upload_path}",
                data=file_content,
                headers={
                    **self.storage_headers,
                    "Content-Type": content_type
                },
                timeout=30
            )
            
            if response.status_code == 200:
                # Return public URL
                public_url = f"{self.url}/storage/v1/object/public/{bucket_name}/{upload_path}"
                print(f"✅ Profile picture uploaded: {public_url}")
                return public_url
            else:
                print(f"❌ Profile picture upload failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error uploading profile picture: {e}")
            return None
    
    def delete_file(self, bucket_name: str, file_path: str) -> bool:
        """Delete file from Supabase storage"""
        try:
            response = self.connection_pool.delete(
                f"{self.url}/storage/v1/object/{bucket_name}/{file_path}",
                headers=self.storage_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ File deleted: {file_path}")
                return True
            else:
                print(f"❌ Delete failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def list_files(self, bucket_name: str, folder: str = "") -> List[Dict[str, Any]]:
        """List files in a bucket"""
        try:
            response = self.connection_pool.get(
                f"{self.url}/storage/v1/object/list/{bucket_name}",
                params={"prefix": folder} if folder else {},
                headers=self.storage_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def get_file_url(self, bucket_name: str, file_path: str) -> str:
        """Get public URL for a file"""
        return f"{self.url}/storage/v1/object/public/{bucket_name}/{file_path}"
    
    def setup_storage_buckets(self) -> bool:
        """Setup required storage buckets"""
        try:
            print("🪣 Setting up Supabase storage buckets...")
            
            # Create certificates bucket
            if not self.create_bucket("certificates", public=True):
                print("⚠️  Certificates bucket creation failed or already exists")
            
            # Create profile-pictures bucket
            if not self.create_bucket("profile-pictures", public=True):
                print("⚠️  Profile pictures bucket creation failed or already exists")
            
            # Create documents bucket
            if not self.create_bucket("documents", public=True):
                print("⚠️  Documents bucket creation failed or already exists")
            
            print("✅ Storage buckets setup completed")
            return True
        except Exception as e:
            print(f"Error setting up storage buckets: {e}")
            return False

# Global fast Supabase client instance
supabase_fast = SupabaseFastClient()
