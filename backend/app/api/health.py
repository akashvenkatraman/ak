from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
import time

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "certificate-management-portal"
    }

@router.get("/database")
def database_health_check(db: Session = Depends(get_db)):
    """Database health check"""
    try:
        # Test database connection
        result = db.execute(text("SELECT 1")).fetchone()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": time.time()
        }

@router.get("/detailed")
def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with database stats"""
    try:
        # Test database connection
        result = db.execute(text("SELECT 1")).fetchone()
        
        # Get user count
        user_count = db.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0]
        admin_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'admin'")).fetchone()[0]
        
        return {
            "status": "healthy",
            "database": "connected",
            "users": user_count,
            "admins": admin_count,
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": time.time()
        }





