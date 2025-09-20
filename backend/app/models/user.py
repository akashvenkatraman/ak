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

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class UserStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String, nullable=True)
    department = Column(String, nullable=True)
    student_id = Column(String, nullable=True)  # For students
    employee_id = Column(String, nullable=True)  # For teachers
    performance_score = Column(Integer, default=0)  # For students - cumulative performance score
    total_credits_earned = Column(Integer, default=0)  # For students - total credits earned
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships will be defined after all models are loaded

class TeacherStudentAllocation(Base):
    __tablename__ = "teacher_student_allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    allocated_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Admin who allocated
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships will be defined after all models are loaded
