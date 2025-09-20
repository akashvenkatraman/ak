from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.notification import Notification
from app.services.notification_service import NotificationService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class NotificationResponse(BaseModel):
    id: int
    notification_type: str
    title: str
    message: str
    is_read: bool
    related_activity_id: int = None
    related_user_id: int = None
    created_at: datetime
    read_at: datetime = None
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    unread_only: bool = False,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notifications for the current user"""
    notification_service = NotificationService(db)
    notifications = notification_service.get_user_notifications(
        user_id=current_user.id,
        unread_only=unread_only,
        limit=limit
    )
    
    return notifications

@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread notifications for the current user"""
    unread_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    
    return {"unread_count": unread_count}

@router.put("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a specific notification as read"""
    notification_service = NotificationService(db)
    success = notification_service.mark_notification_as_read(notification_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return {"message": "Notification marked as read"}

@router.put("/mark-all-read")
def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read for the current user"""
    notification_service = NotificationService(db)
    updated_count = notification_service.mark_all_notifications_as_read(current_user.id)
    
    return {"message": f"Marked {updated_count} notifications as read"}
