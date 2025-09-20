from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Import base from database module to ensure consistency
try:
    from app.core.database import Base
except ImportError:
    Base = declarative_base()

class ActivityType(str, enum.Enum):
    SEMINAR = "seminar"
    CONFERENCE = "conference"
    ONLINE_COURSE = "online_course"
    MOOC = "mooc"
    INTERNSHIP = "internship"
    EXTRACURRICULAR = "extracurricular"
    WORKSHOP = "workshop"
    CERTIFICATION = "certification"

class ActivityStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    activity_type = Column(Enum(ActivityType), nullable=False)
    credits = Column(Float, default=0.0)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    certificate_file_path = Column(String, nullable=True)  # Legacy field for backward compatibility
    additional_documents = Column(Text, nullable=True)  # JSON string for multiple files
    files_count = Column(Integer, default=0)  # Count of uploaded files
    status = Column(Enum(ActivityStatus), default=ActivityStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships will be defined after all models are loaded

class ActivityApproval(Base):
    __tablename__ = "activity_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ActivityStatus), nullable=False)
    comments = Column(Text, nullable=True)
    credits_awarded = Column(Float, default=0.0)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships will be defined after all models are loaded

class StudentPerformance(Base):
    __tablename__ = "student_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    semester = Column(String, nullable=False)
    academic_year = Column(String, nullable=False)
    gpa = Column(Float, nullable=True)
    attendance_percentage = Column(Float, nullable=True)
    total_credits = Column(Float, default=0.0)
    extracurricular_credits = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("User")
