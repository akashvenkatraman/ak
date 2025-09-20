from pydantic import BaseModel
from typing import Optional

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
    recent_submissions: list
