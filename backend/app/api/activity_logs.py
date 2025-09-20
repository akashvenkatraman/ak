from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.auth import get_current_user, get_admin_user, get_teacher_user
from app.models.user import User
from app.models.activity_log import ActivityLog, ActivityLogType
from app.schemas.activity_log import ActivityLogResponse, ActivityLogSummary
from sqlalchemy import func, desc

router = APIRouter(prefix="/activity-logs", tags=["activity-logs"])

@router.get("/activity/{activity_id}", response_model=List[ActivityLogResponse])
def get_activity_logs(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get logs for a specific activity"""
    
    # Check if user has permission to view this activity's logs
    from app.models.activity import Activity
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions
    if (current_user.role not in ["admin", "teacher"] and 
        activity.student_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view these logs"
        )
    
    # Get logs
    logs = db.query(ActivityLog).filter(
        ActivityLog.activity_id == activity_id
    ).order_by(desc(ActivityLog.created_at)).all()
    
    # Add user names
    result = []
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        log_data = ActivityLogResponse.from_orm(log)
        log_data.user_name = user.full_name if user else "Unknown"
        result.append(log_data)
    
    return result

@router.get("/my-logs", response_model=List[ActivityLogResponse])
def get_my_activity_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0)
):
    """Get current user's activity logs"""
    
    logs = db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id
    ).order_by(desc(ActivityLog.created_at)).offset(offset).limit(limit).all()
    
    result = []
    for log in logs:
        log_data = ActivityLogResponse.from_orm(log)
        log_data.user_name = current_user.full_name
        result.append(log_data)
    
    return result

@router.get("/admin/all-logs", response_model=List[ActivityLogResponse])
def get_all_activity_logs(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
    log_type: Optional[ActivityLogType] = Query(None),
    user_id: Optional[int] = Query(None),
    activity_id: Optional[int] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0)
):
    """Get all activity logs (admin only)"""
    
    query = db.query(ActivityLog)
    
    if log_type:
        query = query.filter(ActivityLog.log_type == log_type)
    
    if user_id:
        query = query.filter(ActivityLog.user_id == user_id)
    
    if activity_id:
        query = query.filter(ActivityLog.activity_id == activity_id)
    
    logs = query.order_by(desc(ActivityLog.created_at)).offset(offset).limit(limit).all()
    
    # Add user names
    result = []
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        log_data = ActivityLogResponse.from_orm(log)
        log_data.user_name = user.full_name if user else "Unknown"
        result.append(log_data)
    
    return result

@router.get("/teacher/student-logs", response_model=List[ActivityLogResponse])
def get_student_activity_logs(
    current_teacher: User = Depends(get_teacher_user),
    db: Session = Depends(get_db),
    student_id: Optional[int] = Query(None),
    activity_id: Optional[int] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0)
):
    """Get activity logs for students assigned to the teacher"""
    
    # Get assigned student IDs
    from app.models.user import TeacherStudentAllocation
    allocations = db.query(TeacherStudentAllocation).filter(
        TeacherStudentAllocation.teacher_id == current_teacher.id
    ).all()
    
    assigned_student_ids = [allocation.student_id for allocation in allocations]
    
    if not assigned_student_ids:
        return []
    
    # Build query
    query = db.query(ActivityLog).join(
        Activity, ActivityLog.activity_id == Activity.id
    ).filter(Activity.student_id.in_(assigned_student_ids))
    
    if student_id:
        if student_id not in assigned_student_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student is not assigned to you"
            )
        query = query.filter(Activity.student_id == student_id)
    
    if activity_id:
        query = query.filter(ActivityLog.activity_id == activity_id)
    
    logs = query.order_by(desc(ActivityLog.created_at)).offset(offset).limit(limit).all()
    
    # Add user names
    result = []
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        log_data = ActivityLogResponse.from_orm(log)
        log_data.user_name = user.full_name if user else "Unknown"
        result.append(log_data)
    
    return result

@router.get("/summary", response_model=ActivityLogSummary)
def get_activity_log_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365)
):
    """Get activity log summary for the current user"""
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get logs for the user
    logs = db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id,
        ActivityLog.created_at >= start_date,
        ActivityLog.created_at <= end_date
    ).all()
    
    # Calculate statistics
    total_logs = len(logs)
    logs_by_type = {}
    for log in logs:
        log_type = log.log_type.value if hasattr(log.log_type, 'value') else str(log.log_type)
        logs_by_type[log_type] = logs_by_type.get(log_type, 0) + 1
    
    # Get recent logs
    recent_logs = db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id
    ).order_by(desc(ActivityLog.created_at)).limit(10).all()
    
    recent_logs_data = []
    for log in recent_logs:
        log_data = ActivityLogResponse.from_orm(log)
        log_data.user_name = current_user.full_name
        recent_logs_data.append(log_data)
    
    # Get activity stats
    from app.models.activity import Activity
    if current_user.role == "student":
        activities = db.query(Activity).filter(Activity.student_id == current_user.id).all()
    elif current_user.role == "teacher":
        # Get activities from assigned students
        from app.models.user import TeacherStudentAllocation
        allocations = db.query(TeacherStudentAllocation).filter(
            TeacherStudentAllocation.teacher_id == current_user.id
        ).all()
        assigned_student_ids = [allocation.student_id for allocation in allocations]
        activities = db.query(Activity).filter(Activity.student_id.in_(assigned_student_ids)).all()
    else:  # admin
        activities = db.query(Activity).all()
    
    activity_stats = {
        "total_activities": len(activities),
        "pending_activities": len([a for a in activities if a.status.value == "pending"]),
        "approved_activities": len([a for a in activities if a.status.value == "approved"]),
        "rejected_activities": len([a for a in activities if a.status.value == "rejected"])
    }
    
    return ActivityLogSummary(
        total_logs=total_logs,
        logs_by_type=logs_by_type,
        recent_logs=recent_logs_data,
        activity_stats=activity_stats
    )

@router.get("/admin/summary", response_model=ActivityLogSummary)
def get_admin_activity_log_summary(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365)
):
    """Get system-wide activity log summary (admin only)"""
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get all logs in the date range
    logs = db.query(ActivityLog).filter(
        ActivityLog.created_at >= start_date,
        ActivityLog.created_at <= end_date
    ).all()
    
    # Calculate statistics
    total_logs = len(logs)
    logs_by_type = {}
    for log in logs:
        log_type = log.log_type.value if hasattr(log.log_type, 'value') else str(log.log_type)
        logs_by_type[log_type] = logs_by_type.get(log_type, 0) + 1
    
    # Get recent logs
    recent_logs = db.query(ActivityLog).order_by(desc(ActivityLog.created_at)).limit(20).all()
    
    recent_logs_data = []
    for log in recent_logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        log_data = ActivityLogResponse.from_orm(log)
        log_data.user_name = user.full_name if user else "Unknown"
        recent_logs_data.append(log_data)
    
    # Get system-wide activity stats
    from app.models.activity import Activity
    activities = db.query(Activity).all()
    
    activity_stats = {
        "total_activities": len(activities),
        "pending_activities": len([a for a in activities if a.status.value == "pending"]),
        "approved_activities": len([a for a in activities if a.status.value == "approved"]),
        "rejected_activities": len([a for a in activities if a.status.value == "rejected"])
    }
    
    return ActivityLogSummary(
        total_logs=total_logs,
        logs_by_type=logs_by_type,
        recent_logs=recent_logs_data,
        activity_stats=activity_stats
    )
