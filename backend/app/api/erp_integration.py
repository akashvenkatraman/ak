"""
SVCE ERP Integration API Endpoints
Handles integration with Sri Venkateswara College of Engineering ERP system
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core.database import get_db
from app.core.auth import get_admin_user
from app.models.user import User
from app.services.erp_integration_service import erp_service

router = APIRouter(prefix="/admin/erp", tags=["ERP Integration"])

@router.post("/authenticate")
async def authenticate_with_erp(
    username: str,
    password: str,
    captcha: str,
    current_user: User = Depends(get_admin_user)
):
    """Authenticate with SVCE ERP system"""
    try:
        success = await erp_service.authenticate(username, password, captcha)
        if success:
            return {"message": "Successfully authenticated with SVCE ERP", "status": "success"}
        else:
            raise HTTPException(status_code=401, detail="Failed to authenticate with ERP")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ERP authentication error: {str(e)}")

@router.post("/sync")
async def sync_with_erp(
    current_user: User = Depends(get_admin_user)
):
    """Perform full synchronization with SVCE ERP"""
    try:
        results = await erp_service.full_sync()
        return {
            "message": "ERP synchronization completed",
            "results": results,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ERP sync error: {str(e)}")

@router.get("/students")
async def get_erp_students(
    current_user: User = Depends(get_admin_user)
):
    """Fetch students from SVCE ERP"""
    try:
        students = await erp_service.fetch_students()
        return {"students": students, "count": len(students)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch ERP students: {str(e)}")

@router.get("/teachers")
async def get_erp_teachers(
    current_user: User = Depends(get_admin_user)
):
    """Fetch teachers from SVCE ERP"""
    try:
        teachers = await erp_service.fetch_teachers()
        return {"teachers": teachers, "count": len(teachers)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch ERP teachers: {str(e)}")

@router.get("/certificates")
async def get_erp_certificates(
    current_user: User = Depends(get_admin_user)
):
    """Fetch certificates from SVCE ERP"""
    try:
        certificates = await erp_service.fetch_certificates()
        return {"certificates": certificates, "count": len(certificates)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch ERP certificates: {str(e)}")

@router.get("/status")
async def get_erp_status(
    current_user: User = Depends(get_admin_user)
):
    """Get ERP integration status"""
    try:
        return {
            "authenticated": erp_service.session_token is not None,
            "base_url": erp_service.erp_base_url,
            "status": "active" if erp_service.session_token else "not_authenticated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get ERP status: {str(e)}")
