from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Import base from database module to ensure consistency
try:
    from app.core.database import Base
except ImportError:
    Base = declarative_base()

class ActivityLogType(str, enum.Enum):
    ACTIVITY_CREATED = "activity_created"
    ACTIVITY_UPDATED = "activity_updated"
    ACTIVITY_DELETED = "activity_deleted"
    ACTIVITY_SUBMITTED = "activity_submitted"
    ACTIVITY_APPROVED = "activity_approved"
    ACTIVITY_REJECTED = "activity_rejected"
    ACTIVITY_UNDER_REVIEW = "activity_under_review"
    CERTIFICATE_UPLOADED = "certificate_uploaded"
    CERTIFICATE_VIEWED = "certificate_viewed"
    CERTIFICATE_DOWNLOADED = "certificate_downloaded"
    COMMENT_ADDED = "comment_added"
    CREDITS_AWARDED = "credits_awarded"
    STATUS_CHANGED = "status_changed"

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who performed the action
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Target user if different
    log_type = Column(Enum(ActivityLogType), nullable=False)
    action = Column(Text, nullable=False)  # Description of the action
    details = Column(JSON, nullable=True)  # Store additional data like file paths, old/new values, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    activity = relationship("Activity")
    user = relationship("User", foreign_keys=[user_id])
    target_user = relationship("User", foreign_keys=[target_user_id])

class FileStorage(Base):
    __tablename__ = "file_storage"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    file_name = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_type = Column(String, nullable=False)  # MIME type
    file_extension = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_certificate = Column(Boolean, default=True)
    download_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    activity = relationship("Activity")
    uploader = relationship("User")
