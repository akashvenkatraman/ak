from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.services.oauth_service import google_oauth_service
from app.services.email_service import email_service
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import text

router = APIRouter()

class GoogleAuthRequest(BaseModel):
    authorization_code: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetVerify(BaseModel):
    email: EmailStr
    verification_code: str
    new_password: str

@router.get("/auth/google")
async def google_auth():
    """Initiate Google OAuth authentication"""
    try:
        authorization_url = google_oauth_service.get_authorization_url()
        return {"authorization_url": authorization_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initiating Google OAuth: {str(e)}"
        )

@router.post("/auth/google/callback")
async def google_callback(auth_request: GoogleAuthRequest):
    """Handle Google OAuth callback and authenticate user"""
    try:
        result = await google_oauth_service.authenticate_user(auth_request.authorization_code)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google authentication failed"
            )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing Google OAuth: {str(e)}"
        )

@router.post("/auth/forgot-password")
async def forgot_password(reset_request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Send password reset verification code to user's email"""
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == reset_request.email).first()
        if not user:
            # Don't reveal if email exists or not for security
            return {"message": "If the email exists, a verification code has been sent"}
        
        # Generate verification code
        verification_code = email_service.generate_verification_code()
        
        # Send email
        success = await email_service.send_password_reset_email(
            reset_request.email, 
            verification_code, 
            db
        )
        
        if success:
            return {"message": "If the email exists, a verification code has been sent"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send verification email"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing password reset: {str(e)}"
        )

@router.post("/auth/reset-password")
async def reset_password(reset_data: PasswordResetVerify, db: Session = Depends(get_db)):
    """Reset password using verification code"""
    try:
        # Verify the code
        if not email_service.verify_code(reset_data.email, reset_data.verification_code, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification code"
            )
        
        # Update password
        from app.core.auth import get_password_hash
        hashed_password = get_password_hash(reset_data.new_password)
        
        db.execute(text("""
            UPDATE users 
            SET hashed_password = :password, updated_at = NOW()
            WHERE email = :email
        """), {
            "password": hashed_password,
            "email": reset_data.email
        })
        db.commit()
        
        return {"message": "Password reset successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error resetting password: {str(e)}"
        )

@router.get("/auth/google/url")
async def get_google_auth_url():
    """Get Google OAuth URL for frontend"""
    try:
        authorization_url = google_oauth_service.get_authorization_url()
        return {"url": authorization_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting Google OAuth URL: {str(e)}"
        )
