from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from app.core.database import get_db
from app.core.auth import get_current_user, get_teacher_user, get_admin_user
from app.models.user import User
from app.models.activity import Activity
from app.models.activity_log import FileStorage
from app.schemas.activity_log import FileStorageResponse, FileDownloadResponse, ActivityWithFiles
from app.services.file_manager import file_manager
from config import settings

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload/{activity_id}", response_model=FileStorageResponse)
async def upload_file(
    activity_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a file for an activity"""
    
    # Check if activity exists and user has permission
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user is the student who created the activity or admin
    if current_user.role.lower() != "admin" and activity.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only upload files for your own activities"
        )
    
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Check file size (10MB limit)
    file_content = await file.read()
    if len(file_content) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large. Maximum 10MB allowed."
        )
    
    # Reset file pointer
    await file.seek(0)
    
    # Save file
    return file_manager.save_file(file, activity_id, current_user.id, db)

@router.get("/activity/{activity_id}", response_model=List[FileStorageResponse])
def get_activity_files(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all files for an activity"""
    
    # Check if activity exists
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions
    if (current_user.role.lower() not in ["admin", "teacher"] and 
        activity.student_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view these files"
        )
    
    return file_manager.get_activity_files(activity_id, db)

@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download a file"""
    
    # Get file info
    file_storage = db.query(FileStorage).filter(FileStorage.id == file_id).first()
    if not file_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check permissions
    activity = db.query(Activity).filter(Activity.id == file_storage.activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user has permission to download
    if (current_user.role.lower() not in ["admin", "teacher"] and 
        activity.student_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to download this file"
        )
    
    # Get file path and download
    file_path, original_name, file_type = file_manager.download_file(file_id, db)
    
    return FileResponse(
        path=file_path,
        filename=original_name,
        media_type=file_type
    )

@router.get("/view/{file_id}")
def view_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """View a file (for preview)"""
    
    # Get file info
    file_storage = db.query(FileStorage).filter(FileStorage.id == file_id).first()
    if not file_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check permissions
    activity = db.query(Activity).filter(Activity.id == file_storage.activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user has permission to view
    if (current_user.role.lower() not in ["admin", "teacher"] and 
        activity.student_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this file"
        )
    
    # Increment view count
    file_storage.view_count += 1
    db.commit()
    
    # Log the view
    from app.models.activity_log import ActivityLog, ActivityLogType
    log = ActivityLog(
        activity_id=file_storage.activity_id,
        user_id=current_user.id,
        log_type=ActivityLogType.CERTIFICATE_VIEWED.value,  # Convert enum to string value
        action=f"File '{file_storage.original_name}' viewed",
        details={
            "file_id": file_storage.id,
            "file_name": file_storage.original_name
        }
    )
    db.add(log)
    db.commit()
    
    # Return file info for preview
    return FileStorageResponse.from_orm(file_storage)

@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a file"""
    
    # Get file info
    file_storage = db.query(FileStorage).filter(FileStorage.id == file_id).first()
    if not file_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check permissions
    activity = db.query(Activity).filter(Activity.id == file_storage.activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Only the student who uploaded or admin can delete
    if (current_user.role != "admin" and 
        file_storage.uploaded_by != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own files"
        )
    
    # Delete file
    success = file_manager.delete_file(file_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file"
        )
    
    return {"message": "File deleted successfully"}

@router.get("/activity/{activity_id}/with-files", response_model=ActivityWithFiles)
def get_activity_with_files(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get activity with all its files"""
    
    # Get activity
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions
    if (current_user.role.lower() not in ["admin", "teacher"] and 
        activity.student_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this activity"
        )
    
    # Get files
    files = file_manager.get_activity_files(activity_id, db)
    
    # Get student name
    from app.models.user import User
    student = db.query(User).filter(User.id == activity.student_id).first()
    student_name = student.full_name if student else "Unknown"
    
    # Create response
    activity_data = ActivityWithFiles(
        id=activity.id,
        student_id=activity.student_id,
        student_name=student_name,
        title=activity.title,
        description=activity.description,
        activity_type=activity.activity_type.value if hasattr(activity.activity_type, 'value') else str(activity.activity_type),
        credits=activity.credits,
        start_date=activity.start_date,
        end_date=activity.end_date,
        status=activity.status.value if hasattr(activity.status, 'value') else str(activity.status),
        files_count=activity.files_count,
        files=files,
        created_at=activity.created_at,
        updated_at=activity.updated_at
    )
    
    return activity_data
