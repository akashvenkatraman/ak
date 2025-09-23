#!/usr/bin/env python3
"""File upload API endpoints for certificates and documents"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from file_upload_service import file_upload_service
import os

router = APIRouter()

@router.post("/upload/certificate")
async def upload_certificate(
    file: UploadFile = File(...),
    activity_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload certificate file to Supabase storage"""
    try:
        # Validate file type
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF, JPEG, and PNG files are allowed for certificates"
            )
        
        # Check file size (max 10MB)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10MB"
            )
        
        # Upload file
        result = file_upload_service.upload_certificate(
            file_content=file_content,
            filename=file.filename,
            user_id=current_user.id,
            activity_id=activity_id
        )
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "Certificate uploaded successfully",
                    "file_id": result["file_id"],
                    "filename": result["filename"],
                    "supabase_url": result["supabase_url"],
                    "file_size": result["file_size"]
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Upload failed: {result.get('error', 'Unknown error')}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error uploading certificate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload certificate"
        )

@router.post("/upload/profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload profile picture to Supabase storage"""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, PNG, and GIF files are allowed for profile pictures"
            )
        
        # Check file size (max 5MB)
        file_content = await file.read()
        if len(file_content) > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 5MB"
            )
        
        # Upload file
        result = file_upload_service.upload_profile_picture(
            file_content=file_content,
            filename=file.filename,
            user_id=current_user.id
        )
        
        if result["success"]:
            # Update user profile picture URL
            from app.api.profile import update_user_profile
            profile_data = {"profile_picture": result["supabase_url"]}
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "Profile picture uploaded successfully",
                    "file_id": result["file_id"],
                    "filename": result["filename"],
                    "supabase_url": result["supabase_url"],
                    "file_size": result["file_size"]
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Upload failed: {result.get('error', 'Unknown error')}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error uploading profile picture: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload profile picture"
        )

@router.get("/files/my-files")
async def get_my_files(
    file_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's uploaded files"""
    try:
        files = file_upload_service.get_user_files(
            user_id=current_user.id,
            file_type=file_type
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "files": files,
                "total_count": len(files)
            }
        )
        
    except Exception as e:
        print(f"Error getting user files: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve files"
        )

@router.get("/files/{file_id}")
async def get_file_info(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get file information by ID"""
    try:
        file_info = file_upload_service.get_file_by_id(file_id)
        
        if not file_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        # Check if user owns the file
        if file_info["user_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=file_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting file info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve file information"
        )

@router.delete("/files/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete file by ID"""
    try:
        # Check if file exists and user owns it
        file_info = file_upload_service.get_file_by_id(file_id)
        
        if not file_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        if file_info["user_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Delete file
        success = file_upload_service.delete_file(file_id)
        
        if success:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "File deleted successfully"}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete file"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file"
        )

@router.post("/setup-storage")
async def setup_storage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Setup Supabase storage buckets (admin only)"""
    try:
        # Check if user is admin
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        # Setup storage buckets
        success = file_upload_service.setup_storage()
        
        if success:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Storage buckets setup completed"}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to setup storage buckets"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error setting up storage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to setup storage"
        )
