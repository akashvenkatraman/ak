"""
Supabase Storage Service for User-Specific Image Storage
Handles file uploads, downloads, and management with proper user isolation
"""

import os
import uuid
import requests
from typing import Dict, List, Optional, Any, BinaryIO
from datetime import datetime
from config import settings
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User

class SupabaseStorageService:
    def __init__(self):
        self.url = settings.supabase_url
        self.key = settings.supabase_key
        self.service_key = settings.supabase_service_key
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        self.service_headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json"
        }
    
    def _generate_file_path(self, user_id: int, bucket_name: str, filename: str, activity_id: Optional[int] = None) -> str:
        """Generate a unique file path for user-specific storage"""
        # Create user-specific folder structure
        if activity_id:
            return f"{user_id}/activities/{activity_id}/{uuid.uuid4()}_{filename}"
        else:
            return f"{user_id}/{uuid.uuid4()}_{filename}"
    
    def _validate_file(self, file_content: bytes, allowed_types: List[str], max_size: int) -> Dict[str, Any]:
        """Validate uploaded file"""
        # Check file size
        if len(file_content) > max_size:
            return {
                "valid": False,
                "error": f"File size exceeds {max_size // (1024*1024)}MB limit"
            }
        
        # Check file type (basic validation)
        file_signatures = {
            b'\xff\xd8\xff': 'image/jpeg',
            b'\x89PNG\r\n\x1a\n': 'image/png',
            b'GIF87a': 'image/gif',
            b'GIF89a': 'image/gif',
            b'%PDF': 'application/pdf',
            b'PK\x03\x04': 'application/zip'  # Also covers .docx
        }
        
        detected_type = None
        for signature, mime_type in file_signatures.items():
            if file_content.startswith(signature):
                detected_type = mime_type
                break
        
        if detected_type and detected_type in allowed_types:
            return {"valid": True, "detected_type": detected_type}
        else:
            return {
                "valid": False,
                "error": f"File type not allowed. Allowed types: {', '.join(allowed_types)}"
            }
    
    def upload_user_image(self, user_id: int, file_content: bytes, filename: str, 
                         activity_id: Optional[int] = None) -> Dict[str, Any]:
        """Upload image to user-specific folder in Supabase storage"""
        try:
            # Validate file
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
            max_size = 10 * 1024 * 1024  # 10MB
            
            validation = self._validate_file(file_content, allowed_types, max_size)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            # Generate file path
            file_path = self._generate_file_path(user_id, "user-images", filename, activity_id)
            
            # Upload to Supabase storage
            upload_url = f"{self.url}/storage/v1/object/user-images/{file_path}"
            
            upload_headers = {
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": validation["detected_type"]
            }
            
            response = requests.post(
                upload_url,
                headers=upload_headers,
                data=file_content,
                timeout=30
            )
            
            if response.status_code == 200:
                # Get public URL
                public_url = f"{self.url}/storage/v1/object/public/user-images/{file_path}"
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "public_url": public_url,
                    "file_size": len(file_content),
                    "file_type": validation["detected_type"],
                    "uploaded_at": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Upload failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Upload error: {str(e)}"}
    
    def upload_profile_picture(self, user_id: int, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Upload profile picture to user-specific folder"""
        try:
            # Validate file
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
            max_size = 5 * 1024 * 1024  # 5MB
            
            validation = self._validate_file(file_content, allowed_types, max_size)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            # Generate file path
            file_path = self._generate_file_path(user_id, "profile-pictures", filename)
            
            # Upload to Supabase storage
            upload_url = f"{self.url}/storage/v1/object/profile-pictures/{file_path}"
            
            upload_headers = {
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": validation["detected_type"]
            }
            
            response = requests.post(
                upload_url,
                headers=upload_headers,
                data=file_content,
                timeout=30
            )
            
            if response.status_code == 200:
                # Get public URL
                public_url = f"{self.url}/storage/v1/object/public/profile-pictures/{file_path}"
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "public_url": public_url,
                    "file_size": len(file_content),
                    "file_type": validation["detected_type"],
                    "uploaded_at": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Upload failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Upload error: {str(e)}"}
    
    def upload_activity_document(self, user_id: int, file_content: bytes, filename: str, 
                                activity_id: int) -> Dict[str, Any]:
        """Upload activity-related document"""
        try:
            # Validate file
            allowed_types = [
                "application/pdf",
                "image/jpeg", "image/jpg", "image/png",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ]
            max_size = 15 * 1024 * 1024  # 15MB
            
            validation = self._validate_file(file_content, allowed_types, max_size)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            # Generate file path
            file_path = self._generate_file_path(user_id, "activity-documents", filename, activity_id)
            
            # Upload to Supabase storage
            upload_url = f"{self.url}/storage/v1/object/activity-documents/{file_path}"
            
            upload_headers = {
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": validation["detected_type"]
            }
            
            response = requests.post(
                upload_url,
                headers=upload_headers,
                data=file_content,
                timeout=30
            )
            
            if response.status_code == 200:
                # Get public URL
                public_url = f"{self.url}/storage/v1/object/public/activity-documents/{file_path}"
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "public_url": public_url,
                    "file_size": len(file_content),
                    "file_type": validation["detected_type"],
                    "activity_id": activity_id,
                    "uploaded_at": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Upload failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Upload error: {str(e)}"}
    
    def get_user_files(self, user_id: int, bucket_name: str = "user-images") -> List[Dict[str, Any]]:
        """Get all files for a specific user"""
        try:
            # List files in user's folder
            list_url = f"{self.url}/storage/v1/object/list/{bucket_name}"
            
            list_data = {
                "prefix": f"{user_id}/",
                "limit": 100
            }
            
            response = requests.post(
                list_url,
                headers=self.headers,
                json=list_data,
                timeout=10
            )
            
            if response.status_code == 200:
                files = response.json()
                result = []
                
                for file_info in files:
                    result.append({
                        "name": file_info.get("name", ""),
                        "size": file_info.get("metadata", {}).get("size", 0),
                        "last_modified": file_info.get("updated_at", ""),
                        "public_url": f"{self.url}/storage/v1/object/public/{bucket_name}/{file_info.get('name', '')}"
                    })
                
                return result
            else:
                return []
                
        except Exception as e:
            print(f"Error getting user files: {e}")
            return []
    
    def delete_file(self, file_path: str, bucket_name: str) -> bool:
        """Delete a file from storage"""
        try:
            delete_url = f"{self.url}/storage/v1/object/{bucket_name}/{file_path}"
            
            response = requests.delete(
                delete_url,
                headers=self.headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def get_file_info(self, file_path: str, bucket_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific file"""
        try:
            info_url = f"{self.url}/storage/v1/object/info/{bucket_name}/{file_path}"
            
            response = requests.get(
                info_url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None

# Global storage service instance
storage_service = SupabaseStorageService()
