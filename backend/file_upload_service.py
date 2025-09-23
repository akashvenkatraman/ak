#!/usr/bin/env python3
"""File upload service for certificates and documents using Supabase storage"""

import os
import uuid
import mimetypes
from typing import Optional, Dict, Any, BinaryIO, List
from datetime import datetime
from supabase_fast_client import supabase_fast
from app.core.database import SessionLocal
from sqlalchemy import text

class FileUploadService:
    def __init__(self):
        self.supabase = supabase_fast
        self.local_uploads_dir = "uploads"
        self.certificates_dir = os.path.join(self.local_uploads_dir, "certificates")
        self.profile_pictures_dir = os.path.join(self.local_uploads_dir, "profile_pictures")
        
        # Create local directories
        os.makedirs(self.certificates_dir, exist_ok=True)
        os.makedirs(self.profile_pictures_dir, exist_ok=True)
    
    def upload_certificate(self, file_content: bytes, filename: str, 
                          user_id: int, activity_id: Optional[int] = None) -> Dict[str, Any]:
        """Upload certificate to Supabase storage and local backup"""
        try:
            # Generate unique filename
            file_extension = filename.split('.')[-1] if '.' in filename else 'pdf'
            unique_filename = f"{user_id}_{activity_id or 'general'}_{uuid.uuid4().hex}.{file_extension}"
            
            # Upload to Supabase storage
            supabase_url = self.supabase.upload_certificate(
                filename, file_content, user_id, activity_id
            )
            
            # Save local backup
            local_path = os.path.join(self.certificates_dir, unique_filename)
            with open(local_path, 'wb') as f:
                f.write(file_content)
            
            # Get file info
            file_size = len(file_content)
            content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            
            # Store file metadata in database
            file_record = self._store_file_metadata(
                filename=unique_filename,
                original_filename=filename,
                file_path=local_path,
                supabase_url=supabase_url,
                file_size=file_size,
                content_type=content_type,
                file_type="certificate",
                user_id=user_id,
                activity_id=activity_id
            )
            
            return {
                "success": True,
                "file_id": file_record.get("id"),
                "filename": unique_filename,
                "original_filename": filename,
                "local_path": local_path,
                "supabase_url": supabase_url,
                "file_size": file_size,
                "content_type": content_type,
                "uploaded_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error uploading certificate: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def upload_profile_picture(self, file_content: bytes, filename: str, user_id: int) -> Dict[str, Any]:
        """Upload profile picture to Supabase storage and local backup"""
        try:
            # Generate unique filename
            file_extension = filename.split('.')[-1] if '.' in filename else 'jpg'
            unique_filename = f"{user_id}_{uuid.uuid4().hex}.{file_extension}"
            
            # Upload to Supabase storage
            supabase_url = self.supabase.upload_profile_picture(
                filename, file_content, user_id
            )
            
            # Save local backup
            local_path = os.path.join(self.profile_pictures_dir, unique_filename)
            with open(local_path, 'wb') as f:
                f.write(file_content)
            
            # Get file info
            file_size = len(file_content)
            content_type = mimetypes.guess_type(filename)[0] or 'image/jpeg'
            
            # Store file metadata in database
            file_record = self._store_file_metadata(
                filename=unique_filename,
                original_filename=filename,
                file_path=local_path,
                supabase_url=supabase_url,
                file_size=file_size,
                content_type=content_type,
                file_type="profile_picture",
                user_id=user_id,
                activity_id=None
            )
            
            return {
                "success": True,
                "file_id": file_record.get("id"),
                "filename": unique_filename,
                "original_filename": filename,
                "local_path": local_path,
                "supabase_url": supabase_url,
                "file_size": file_size,
                "content_type": content_type,
                "uploaded_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error uploading profile picture: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _store_file_metadata(self, filename: str, original_filename: str, 
                           file_path: str, supabase_url: Optional[str],
                           file_size: int, content_type: str, file_type: str,
                           user_id: int, activity_id: Optional[int]) -> Dict[str, Any]:
        """Store file metadata in database"""
        try:
            db = SessionLocal()
            
            # Get file extension
            file_extension = filename.split('.')[-1] if '.' in filename else 'pdf'
            
            # Insert file record using existing table structure
            # Use 0 as default activity_id if None to satisfy NOT NULL constraint
            activity_id_value = activity_id if activity_id is not None else 0
            
            result = db.execute(text("""
                INSERT INTO file_storage (
                    file_name, original_name, file_path, file_size, 
                    file_type, file_extension, uploaded_by, activity_id, 
                    is_certificate, created_at, updated_at
                ) VALUES (
                    :filename, :original_filename, :file_path, :file_size,
                    :file_type, :file_extension, :user_id, :activity_id,
                    :is_certificate, datetime('now'), datetime('now')
                )
                RETURNING id, file_name, original_name, file_path, file_size,
                          file_type, file_extension, uploaded_by, activity_id,
                          is_certificate, created_at, updated_at
            """), {
                "filename": filename,
                "original_filename": original_filename,
                "file_path": file_path,
                "file_size": file_size,
                "file_type": file_type,
                "file_extension": file_extension,
                "user_id": user_id,
                "activity_id": activity_id_value,
                "is_certificate": file_type == "certificate"
            })
            
            file_record = result.fetchone()
            db.commit()
            db.close()
            
            return {
                "id": file_record.id,
                "filename": file_record.file_name,
                "original_filename": file_record.original_name,
                "file_path": file_record.file_path,
                "supabase_url": supabase_url,  # Store separately since not in table
                "file_size": file_record.file_size,
                "content_type": content_type,  # Store separately since not in table
                "file_type": file_record.file_type,
                "user_id": file_record.uploaded_by,
                "activity_id": file_record.activity_id,
                "created_at": file_record.created_at,
                "updated_at": file_record.updated_at
            }
            
        except Exception as e:
            print(f"Error storing file metadata: {e}")
            return {}
    
    def get_file_by_id(self, file_id: int) -> Optional[Dict[str, Any]]:
        """Get file metadata by ID"""
        try:
            db = SessionLocal()
            result = db.execute(text("""
                SELECT id, file_name, original_name, file_path, file_size,
                       file_type, file_extension, uploaded_by, activity_id,
                       is_certificate, created_at, updated_at
                FROM file_storage 
                WHERE id = :file_id
            """), {"file_id": file_id})
            
            file_record = result.fetchone()
            db.close()
            
            if file_record:
                return {
                    "id": file_record.id,
                    "filename": file_record.file_name,
                    "original_filename": file_record.original_name,
                    "file_path": file_record.file_path,
                    "supabase_url": None,  # Not stored in current table
                    "file_size": file_record.file_size,
                    "content_type": f"application/{file_record.file_extension}",  # Infer from extension
                    "file_type": file_record.file_type,
                    "user_id": file_record.uploaded_by,
                    "activity_id": file_record.activity_id,
                    "created_at": file_record.created_at,
                    "updated_at": file_record.updated_at
                }
            return None
            
        except Exception as e:
            print(f"Error getting file by ID: {e}")
            return None
    
    def get_user_files(self, user_id: int, file_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all files for a user"""
        try:
            db = SessionLocal()
            
            if file_type:
                result = db.execute(text("""
                    SELECT id, file_name, original_name, file_path, file_size,
                           file_type, file_extension, uploaded_by, activity_id,
                           is_certificate, created_at, updated_at
                    FROM file_storage 
                    WHERE uploaded_by = :user_id AND file_type = :file_type
                    ORDER BY created_at DESC
                """), {"user_id": user_id, "file_type": file_type})
            else:
                result = db.execute(text("""
                    SELECT id, file_name, original_name, file_path, file_size,
                           file_type, file_extension, uploaded_by, activity_id,
                           is_certificate, created_at, updated_at
                    FROM file_storage 
                    WHERE uploaded_by = :user_id
                    ORDER BY created_at DESC
                """), {"user_id": user_id})
            
            files = []
            for row in result.fetchall():
                files.append({
                    "id": row.id,
                    "filename": row.file_name,
                    "original_filename": row.original_name,
                    "file_path": row.file_path,
                    "supabase_url": None,  # Not stored in current table
                    "file_size": row.file_size,
                    "content_type": f"application/{row.file_extension}",  # Infer from extension
                    "file_type": row.file_type,
                    "user_id": row.uploaded_by,
                    "activity_id": row.activity_id,
                    "created_at": row.created_at,
                    "updated_at": row.updated_at
                })
            
            db.close()
            return files
            
        except Exception as e:
            print(f"Error getting user files: {e}")
            return []
    
    def delete_file(self, file_id: int) -> bool:
        """Delete file from both Supabase and local storage"""
        try:
            # Get file metadata
            file_record = self.get_file_by_id(file_id)
            if not file_record:
                return False
            
            # Delete from Supabase storage
            if file_record["supabase_url"]:
                # Extract bucket and path from URL
                url_parts = file_record["supabase_url"].split("/storage/v1/object/public/")
                if len(url_parts) > 1:
                    bucket_path = url_parts[1]
                    bucket_name = bucket_path.split("/")[0]
                    file_path = "/".join(bucket_path.split("/")[1:])
                    self.supabase.delete_file(bucket_name, file_path)
            
            # Delete from local storage
            if os.path.exists(file_record["file_path"]):
                os.remove(file_record["file_path"])
            
            # Delete from database
            db = SessionLocal()
            db.execute(text("DELETE FROM file_storage WHERE id = :file_id"), {"file_id": file_id})
            db.commit()
            db.close()
            
            print(f"✅ File deleted: {file_record['filename']}")
            return True
            
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def setup_storage(self) -> bool:
        """Setup Supabase storage buckets"""
        return self.supabase.setup_storage_buckets()

# Global file upload service instance
file_upload_service = FileUploadService()
