"""
User Storage API Endpoints
Handles user-specific image and document uploads to Supabase storage
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.storage_service import storage_service
import io

router = APIRouter()

@router.post("/upload/user-image")
async def upload_user_image(
    file: UploadFile = File(...),
    activity_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a user image to Supabase storage"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Upload to storage
        result = storage_service.upload_user_image(
            user_id=current_user.id,
            file_content=file_content,
            filename=file.filename or "image",
            activity_id=activity_id
        )
        
        if result["success"]:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Image uploaded successfully",
                    "data": result
                }
            )
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/upload/profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a profile picture to Supabase storage"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Upload to storage
        result = storage_service.upload_profile_picture(
            user_id=current_user.id,
            file_content=file_content,
            filename=file.filename or "profile_picture"
        )
        
        if result["success"]:
            # Update user profile picture in database
            current_user.profile_picture = result["public_url"]
            db.commit()
            db.refresh(current_user)
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Profile picture uploaded successfully",
                    "data": result,
                    "user": {
                        "id": current_user.id,
                        "profile_picture": current_user.profile_picture
                    }
                }
            )
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/upload/activity-document")
async def upload_activity_document(
    file: UploadFile = File(...),
    activity_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload an activity-related document to Supabase storage"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Upload to storage
        result = storage_service.upload_activity_document(
            user_id=current_user.id,
            file_content=file_content,
            filename=file.filename or "document",
            activity_id=activity_id
        )
        
        if result["success"]:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Document uploaded successfully",
                    "data": result
                }
            )
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/files/my-images")
async def get_my_images(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all images uploaded by the current user"""
    try:
        files = storage_service.get_user_files(
            user_id=current_user.id,
            bucket_name="user-images"
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "User images retrieved successfully",
                "data": {
                    "user_id": current_user.id,
                    "files": files,
                    "total_files": len(files)
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve images: {str(e)}")

@router.get("/files/my-documents")
async def get_my_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents uploaded by the current user"""
    try:
        files = storage_service.get_user_files(
            user_id=current_user.id,
            bucket_name="activity-documents"
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "User documents retrieved successfully",
                "data": {
                    "user_id": current_user.id,
                    "files": files,
                    "total_files": len(files)
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve documents: {str(e)}")

@router.get("/files/profile-picture")
async def get_profile_picture(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the current user's profile picture"""
    try:
        files = storage_service.get_user_files(
            user_id=current_user.id,
            bucket_name="profile-pictures"
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Profile picture retrieved successfully",
                "data": {
                    "user_id": current_user.id,
                    "profile_picture_url": current_user.profile_picture,
                    "files": files
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve profile picture: {str(e)}")

@router.delete("/files/delete")
async def delete_file(
    file_path: str = Form(...),
    bucket_name: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a file from storage (only user's own files)"""
    try:
        # Verify the file belongs to the current user
        if not file_path.startswith(f"{current_user.id}/"):
            raise HTTPException(status_code=403, detail="Access denied: You can only delete your own files")
        
        # Delete the file
        success = storage_service.delete_file(file_path, bucket_name)
        
        if success:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "File deleted successfully",
                    "data": {
                        "file_path": file_path,
                        "bucket_name": bucket_name
                    }
                }
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to delete file")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

@router.get("/files/info")
async def get_file_info(
    file_path: str,
    bucket_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get information about a specific file"""
    try:
        # Verify the file belongs to the current user
        if not file_path.startswith(f"{current_user.id}/"):
            raise HTTPException(status_code=403, detail="Access denied: You can only access your own files")
        
        # Get file info
        file_info = storage_service.get_file_info(file_path, bucket_name)
        
        if file_info:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "File information retrieved successfully",
                    "data": file_info
                }
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file info: {str(e)}")

@router.get("/storage/status")
async def get_storage_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get storage status and usage for the current user"""
    try:
        # Get files from all buckets
        user_images = storage_service.get_user_files(current_user.id, "user-images")
        profile_pictures = storage_service.get_user_files(current_user.id, "profile-pictures")
        activity_documents = storage_service.get_user_files(current_user.id, "activity-documents")
        
        # Calculate total storage used
        total_size = 0
        for files in [user_images, profile_pictures, activity_documents]:
            for file in files:
                total_size += file.get("size", 0)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Storage status retrieved successfully",
                "data": {
                    "user_id": current_user.id,
                    "storage_usage": {
                        "total_size_bytes": total_size,
                        "total_size_mb": round(total_size / (1024 * 1024), 2),
                        "user_images_count": len(user_images),
                        "profile_pictures_count": len(profile_pictures),
                        "activity_documents_count": len(activity_documents),
                        "total_files": len(user_images) + len(profile_pictures) + len(activity_documents)
                    },
                    "buckets": {
                        "user_images": user_images,
                        "profile_pictures": profile_pictures,
                        "activity_documents": activity_documents
                    }
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get storage status: {str(e)}")
