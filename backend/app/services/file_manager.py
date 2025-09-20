import os
import uuid
import mimetypes
from typing import List, Optional, Tuple
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.models.activity_log import FileStorage, ActivityLog, ActivityLogType
from app.models.activity import Activity
from app.models.user import User
from app.schemas.activity_log import FileStorageCreate, FileStorageResponse
from datetime import datetime
import json

class FileManager:
    def __init__(self, upload_dir: str = "uploads/certificates"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
    
    def save_file(self, file: UploadFile, activity_id: int, uploaded_by: int, db: Session) -> FileStorageResponse:
        """Save uploaded file and create database record"""
        try:
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(self.upload_dir, unique_filename)
            # Normalize path for cross-platform compatibility
            file_path = os.path.normpath(file_path)
            
            # Get file info
            file_content = file.file.read()
            file_size = len(file_content)
            file_type, _ = mimetypes.guess_type(file.filename)
            file_type = file_type or 'application/octet-stream'
            
            # Save file to disk
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)
            
            # Create database record
            file_storage = FileStorage(
                activity_id=activity_id,
                file_name=unique_filename,
                original_name=file.filename,
                file_path=file_path,
                file_size=file_size,
                file_type=file_type,
                file_extension=file_extension,
                uploaded_by=uploaded_by,
                is_certificate=True
            )
            
            db.add(file_storage)
            db.commit()
            db.refresh(file_storage)
            
            # Update activity file count
            activity = db.query(Activity).filter(Activity.id == activity_id).first()
            if activity:
                activity.files_count = db.query(FileStorage).filter(FileStorage.activity_id == activity_id).count()
                db.commit()
            
            # Log the file upload
            self._log_activity(
                db=db,
                activity_id=activity_id,
                user_id=uploaded_by,
                log_type=ActivityLogType.CERTIFICATE_UPLOADED,
                action=f"File '{file.filename}' uploaded",
                details={
                    "file_id": file_storage.id,
                    "file_name": file.filename,
                    "file_size": file_size,
                    "file_type": file_type
                }
            )
            
            return FileStorageResponse.from_orm(file_storage)
            
        except Exception as e:
            # Clean up file if database operation fails
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
    
    def get_file(self, file_id: int, db: Session) -> Optional[FileStorageResponse]:
        """Get file information by ID"""
        file_storage = db.query(FileStorage).filter(FileStorage.id == file_id).first()
        if not file_storage:
            return None
        
        # Increment view count
        file_storage.view_count += 1
        db.commit()
        
        return FileStorageResponse.from_orm(file_storage)
    
    def get_activity_files(self, activity_id: int, db: Session) -> List[FileStorageResponse]:
        """Get all files for an activity"""
        files = db.query(FileStorage).filter(FileStorage.activity_id == activity_id).all()
        return [FileStorageResponse.from_orm(file) for file in files]
    
    def download_file(self, file_id: int, db: Session) -> Tuple[str, str, str]:
        """Get file path for download and increment download count"""
        file_storage = db.query(FileStorage).filter(FileStorage.id == file_id).first()
        if not file_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        # Normalize the file path for cross-platform compatibility
        normalized_path = os.path.normpath(file_storage.file_path)
        if not os.path.exists(normalized_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found on disk: {normalized_path}"
            )
        
        # Increment download count
        file_storage.download_count += 1
        db.commit()
        
        # Log the download (temporarily disabled due to enum issue)
        # self._log_activity(
        #     db=db,
        #     activity_id=file_storage.activity_id,
        #     user_id=file_storage.uploaded_by,  # This should be the current user, but we'll use uploader for now
        #     log_type=ActivityLogType.CERTIFICATE_DOWNLOADED,
        #     action=f"File '{file_storage.original_name}' downloaded",
        #     details={
        #         "file_id": file_storage.id,
        #         "file_name": file_storage.original_name
        #     }
        # )
        
        return normalized_path, file_storage.original_name, file_storage.file_type
    
    def delete_file(self, file_id: int, db: Session) -> bool:
        """Delete file from disk and database"""
        file_storage = db.query(FileStorage).filter(FileStorage.id == file_id).first()
        if not file_storage:
            return False
        
        # Delete from disk
        if os.path.exists(file_storage.file_path):
            os.remove(file_storage.file_path)
        
        # Delete from database
        db.delete(file_storage)
        db.commit()
        
        # Update activity file count
        activity = db.query(Activity).filter(Activity.id == file_storage.activity_id).first()
        if activity:
            activity.files_count = db.query(FileStorage).filter(FileStorage.activity_id == file_storage.activity_id).count()
            db.commit()
        
        return True
    
    def _log_activity(self, db: Session, activity_id: int, user_id: int, log_type: ActivityLogType, 
                     action: str, details: dict = None):
        """Log activity for audit trail"""
        log = ActivityLog(
            activity_id=activity_id,
            user_id=user_id,
            log_type=log_type,
            action=action,
            details=details
        )
        db.add(log)
        db.commit()
    
    def get_file_download_url(self, file_id: int, base_url: str) -> str:
        """Generate download URL for file"""
        return f"{base_url}/files/download/{file_id}"
    
    def get_file_view_url(self, file_id: int, base_url: str) -> str:
        """Generate view URL for file"""
        return f"{base_url}/files/view/{file_id}"

# Global file manager instance
file_manager = FileManager()
