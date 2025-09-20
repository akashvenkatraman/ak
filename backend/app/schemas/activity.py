from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from app.models.activity import ActivityType, ActivityStatus

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    activity_type: ActivityType
    credits: Optional[float] = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    activity_type: Optional[ActivityType] = None
    credits: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ActivityResponse(ActivityBase):
    id: int
    student_id: int
    student_name: Optional[str] = None
    certificate_file_path: Optional[str] = None
    additional_documents: Optional[str] = None
    status: ActivityStatus
    files_count: Optional[int] = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ActivityApprovalCreate(BaseModel):
    activity_id: int
    status: ActivityStatus
    comments: Optional[str] = None
    credits_awarded: Optional[float] = 0.0

class ActivityApprovalResponse(BaseModel):
    id: int
    activity_id: int
    teacher_id: int
    teacher_name: Optional[str] = None
    status: ActivityStatus
    comments: Optional[str] = None
    credits_awarded: float
    approved_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentPerformanceBase(BaseModel):
    semester: str
    academic_year: str
    gpa: Optional[float] = None
    attendance_percentage: Optional[float] = None
    total_credits: Optional[float] = 0.0
    extracurricular_credits: Optional[float] = 0.0

class StudentPerformanceCreate(StudentPerformanceBase):
    student_id: int

class StudentPerformanceUpdate(BaseModel):
    gpa: Optional[float] = None
    attendance_percentage: Optional[float] = None
    total_credits: Optional[float] = None
    extracurricular_credits: Optional[float] = None

class StudentPerformanceResponse(StudentPerformanceBase):
    id: int
    student_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_activities: int
    pending_activities: int
    approved_activities: int
    rejected_activities: int
    total_credits: float
    performance_score: int
    total_credits_earned: int
    attendance_percentage: Optional[float] = None
    gpa: Optional[float] = None

class TeacherDashboardStats(BaseModel):
    total_students: int
    pending_approvals: int
    total_activities_reviewed: int
    recent_submissions: List[ActivityResponse]

