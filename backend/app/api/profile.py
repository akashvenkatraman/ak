from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileUpdate, ProfileResponse, PasswordChange, ProfilePictureResponse
from app.core.auth import verify_password, get_password_hash

router = APIRouter()

@router.get("/profile/profile", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile information"""
    # Convert User object to dictionary for Pydantic validation
    user_dict = {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "status": current_user.status,
        "phone_number": current_user.phone_number,
        "department": current_user.department,
        "student_id": current_user.student_id,
        "employee_id": current_user.employee_id,
        "performance_score": current_user.performance_score,
        "total_credits_earned": current_user.total_credits_earned,
        "profile_picture": current_user.profile_picture,
        "bio": current_user.bio,
        "date_of_birth": current_user.date_of_birth,
        "address": current_user.address,
        "city": current_user.city,
        "state": current_user.state,
        "country": current_user.country,
        "postal_code": current_user.postal_code,
        "linkedin_url": current_user.linkedin_url,
        "twitter_url": current_user.twitter_url,
        "website_url": current_user.website_url,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }
    return ProfileResponse.model_validate(user_dict)

@router.put("/profile/profile", response_model=ProfileResponse)
def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile information"""
    
    # Check if email is being changed and if it's already taken
    if profile_data.email and profile_data.email != current_user.email:
        existing_user = db.query(User).filter(User.email == profile_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update only provided fields using raw SQL for guaranteed database persistence
    update_data = profile_data.dict(exclude_unset=True)
    
    if update_data:
        # Build dynamic SQL update query
        set_clauses = []
        params = {"user_id": current_user.id}
        
        for field, value in update_data.items():
            if field in ['email', 'username', 'full_name', 'phone_number', 'department', 
                        'student_id', 'employee_id', 'profile_picture', 'bio', 'address', 
                        'city', 'state', 'country', 'postal_code', 'linkedin_url', 
                        'twitter_url', 'website_url', 'performance_score', 'total_credits_earned']:
                set_clauses.append(f"{field} = :{field}")
                params[field] = value
            elif field == 'date_of_birth':
                set_clauses.append(f"{field} = :{field}")
                params[field] = value
        
        if set_clauses:
            set_clauses.append("updated_at = NOW()")
            
            from sqlalchemy import text
            update_query = f"""
                UPDATE users 
                SET {', '.join(set_clauses)}
                WHERE id = :user_id
            """
            
            db.execute(text(update_query), params)
            db.commit()
            
            # Update the current_user object for response
            for field, value in update_data.items():
                if hasattr(current_user, field):
                    setattr(current_user, field, value)
            current_user.updated_at = datetime.utcnow()
    
    # Convert User object to dictionary for Pydantic validation
    user_dict = {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "status": current_user.status,
        "phone_number": current_user.phone_number,
        "department": current_user.department,
        "student_id": current_user.student_id,
        "employee_id": current_user.employee_id,
        "performance_score": current_user.performance_score,
        "total_credits_earned": current_user.total_credits_earned,
        "profile_picture": current_user.profile_picture,
        "bio": current_user.bio,
        "date_of_birth": current_user.date_of_birth,
        "address": current_user.address,
        "city": current_user.city,
        "state": current_user.state,
        "country": current_user.country,
        "postal_code": current_user.postal_code,
        "linkedin_url": current_user.linkedin_url,
        "twitter_url": current_user.twitter_url,
        "website_url": current_user.website_url,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }
    
    return ProfileResponse.model_validate(user_dict)

@router.post("/profile/profile/password", response_model=dict)
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user's password"""
    
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    current_user.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Password updated successfully"}

@router.post("/profile/profile/picture", response_model=ProfilePictureResponse)
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload profile picture"""
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, GIF, and WebP images are allowed"
        )
    
    # Validate file size (5MB max)
    file_size = 0
    content = await file.read()
    file_size = len(content)
    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large. Maximum size is 5MB"
        )
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{current_user.id}_{uuid.uuid4()}{file_extension}"
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads/profile_pictures"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, unique_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Update user's profile picture URL in database
    profile_picture_url = f"/uploads/profile_pictures/{unique_filename}"
    
    # Use raw SQL to update the database directly
    from sqlalchemy import text
    db.execute(text("""
        UPDATE users 
        SET profile_picture = :profile_picture, updated_at = NOW() 
        WHERE id = :user_id
    """), {
        "profile_picture": profile_picture_url,
        "user_id": current_user.id
    })
    db.commit()
    
    # Update the current_user object for response
    current_user.profile_picture = profile_picture_url
    current_user.updated_at = datetime.utcnow()
    
    return ProfilePictureResponse(
        profile_picture=profile_picture_url,
        message="Profile picture uploaded successfully"
    )

@router.delete("/profile/profile/picture", response_model=dict)
def delete_profile_picture(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete current user's profile picture"""
    
    if current_user.profile_picture:
        # Remove file from filesystem
        file_path = current_user.profile_picture.replace("/uploads/profile_pictures/", "uploads/profile_pictures/")
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Update database using raw SQL
        from sqlalchemy import text
        db.execute(text("""
            UPDATE users 
            SET profile_picture = NULL, updated_at = NOW() 
            WHERE id = :user_id
        """), {"user_id": current_user.id})
        db.commit()
        
        # Update the current_user object for response
        current_user.profile_picture = None
        current_user.updated_at = datetime.utcnow()
        
        return {"message": "Profile picture deleted successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No profile picture found"
    )

@router.get("/profile/profile/picture/{user_id}")
def get_profile_picture(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get profile picture by user ID"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.profile_picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile picture found"
        )
    
    file_path = user.profile_picture.replace("/uploads/profile_pictures/", "uploads/profile_pictures/")
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile picture file not found"
        )
    
    return {"profile_picture_url": user.profile_picture}
