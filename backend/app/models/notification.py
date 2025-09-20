from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Import base from database module to ensure consistency
try:
    from app.core.database import Base
except ImportError:
    Base = declarative_base()

class NotificationType(str, enum.Enum):
    ACTIVITY_SUBMITTED = "activity_submitted"
    ACTIVITY_APPROVED = "activity_approved"
    ACTIVITY_REJECTED = "activity_rejected"
    STUDENT_ALLOCATED = "student_allocated"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    related_activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    related_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    related_activity = relationship("Activity", foreign_keys=[related_activity_id])
    related_user = relationship("User", foreign_keys=[related_user_id])
