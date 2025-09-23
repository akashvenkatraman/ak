from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.auth import get_teacher_user
from app.models.user import User, TeacherStudentAllocation
from app.models.activity import Activity, ActivityStatus, ActivityApproval
from app.schemas.activity import (
    ActivityResponse,
    ActivityApprovalCreate,
    ActivityApprovalResponse,
    TeacherDashboardStats
)
from app.schemas.user import UserResponse

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.get("/dashboard", response_model=TeacherDashboardStats)
def get_teacher_dashboard(
    current_teacher: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    """Get teacher dashboard statistics"""
    
    # Get assigned students
    student_allocations = db.query(TeacherStudentAllocation).filter(
        TeacherStudentAllocation.teacher_id == current_teacher.id
    ).all()
    
    student_ids = [allocation.student_id for allocation in student_allocations]
    
    # Get pending activities from assigned students
    pending_activities = db.query(Activity).filter(
        Activity.student_id.in_(student_ids),
        Activity.status == ActivityStatus.PENDING
    ).count()
    
    # Get total activities reviewed by this teacher
    total_reviewed = db.query(ActivityApproval).filter(
        ActivityApproval.teacher_id == current_teacher.id
    ).count()
    
    # Get recent submissions (last 5)
    recent_submissions = db.query(Activity).filter(
        Activity.student_id.in_(student_ids),
        Activity.status == ActivityStatus.PENDING
    ).order_by(Activity.created_at.desc()).limit(5).all()
    
    # Add student names to recent submissions
    recent_submissions_with_names = []
    for activity in recent_submissions:
        student = db.query(User).filter(User.id == activity.student_id).first()
        activity_data = ActivityResponse.from_orm(activity)
        activity_data.student_name = student.full_name if student else "Unknown"
        recent_submissions_with_names.append(activity_data)
    
    return TeacherDashboardStats(
        total_students=len(student_ids),
        pending_approvals=pending_activities,
        total_activities_reviewed=total_reviewed,
        recent_submissions=recent_submissions_with_names
    )

@router.get("/students", response_model=List[UserResponse])
def get_assigned_students(
    current_teacher: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    """Get all students assigned to the current teacher"""
    
    # Get student IDs assigned to this teacher
    student_allocations = db.query(TeacherStudentAllocation).filter(
        TeacherStudentAllocation.teacher_id == current_teacher.id
    ).all()
    
    student_ids = [allocation.student_id for allocation in student_allocations]
    
    # Get student details
    students = db.query(User).filter(User.id.in_(student_ids)).all()
    
    return students

@router.get("/pending-activities", response_model=List[ActivityResponse])
def get_pending_activities(
    student_id: Optional[int] = Query(None),
    current_teacher: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    """Get pending activities from assigned students"""
    
    # Get assigned student IDs
    student_allocations = db.query(TeacherStudentAllocation).filter(
        TeacherStudentAllocation.teacher_id == current_teacher.id
    ).all()
    
    assigned_student_ids = [allocation.student_id for allocation in student_allocations]
    
    # Build query for pending activities
    query = db.query(Activity).filter(
        Activity.student_id.in_(assigned_student_ids),
        Activity.status == ActivityStatus.PENDING
    )
    
    if student_id:
        if student_id not in assigned_student_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student is not assigned to you"
            )
        query = query.filter(Activity.student_id == student_id)
    
    activities = query.order_by(Activity.created_at.desc()).all()
    
    # Add student names and files count
    activities_with_names = []
    for activity in activities:
        student = db.query(User).filter(User.id == activity.student_id).first()
        activity_data = ActivityResponse.from_orm(activity)
        activity_data.student_name = student.full_name if student else "Unknown"
        
        # Get files count
        from app.models.activity_log import FileStorage
        files_count = db.query(FileStorage).filter(FileStorage.activity_id == activity.id).count()
        activity_data.files_count = files_count
        
        activities_with_names.append(activity_data)
    
    return activities_with_names

@router.get("/activities", response_model=List[ActivityResponse])
def get_all_student_activities(
    student_id: Optional[int] = Query(None),
    status: Optional[ActivityStatus] = Query(None),
    current_teacher: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    """Get all activities from assigned students with optional filters"""
    
    # Get assigned student IDs
    student_allocations = db.query(TeacherStudentAllocation).filter(
        TeacherStudentAllocation.teacher_id == current_teacher.id
    ).all()
    
    assigned_student_ids = [allocation.student_id for allocation in student_allocations]
    
    # Build query
    query = db.query(Activity).filter(Activity.student_id.in_(assigned_student_ids))
    
    if student_id:
        if student_id not in assigned_student_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student is not assigned to you"
            )
        query = query.filter(Activity.student_id == student_id)
    
    if status:
        query = query.filter(Activity.status == status)
    
    activities = query.order_by(Activity.created_at.desc()).all()
    
    # Add student names and files count
    activities_with_names = []
    for activity in activities:
        student = db.query(User).filter(User.id == activity.student_id).first()
        activity_data = ActivityResponse.from_orm(activity)
        activity_data.student_name = student.full_name if student else "Unknown"
        
        # Get files count
        from app.models.activity_log import FileStorage
        files_count = db.query(FileStorage).filter(FileStorage.activity_id == activity.id).count()
        activity_data.files_count = files_count
        
        activities_with_names.append(activity_data)
    
    return activities_with_names

@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity_details(
    activity_id: int,
    current_teacher: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    """Get detailed view of a specific activity"""
    
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if the student is assigned to this teacher
    allocation = db.query(TeacherStudentAllocation).filter(
        TeacherStudentAllocation.teacher_id == current_teacher.id,
        TeacherStudentAllocation.student_id == activity.student_id
    ).first()
    
    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this activity"
        )
    
    # Add student name
    student = db.query(User).filter(User.id == activity.student_id).first()
    activity_data = ActivityResponse.from_orm(activity)
    activity_data.student_name = student.full_name if student else "Unknown"
    
    return activity_data

@router.post("/approve-activity", response_model=ActivityApprovalResponse)
def approve_activity(
    approval_data: ActivityApprovalCreate,
    current_teacher: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    """Approve or reject a student activity (teachers can now approve/reject directly)"""
    
    from datetime import datetime
    from sqlalchemy import text
    
    activity = db.query(Activity).filter(Activity.id == approval_data.activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if the student is assigned to this teacher
    allocation = db.query(TeacherStudentAllocation).filter(
        TeacherStudentAllocation.teacher_id == current_teacher.id,
        TeacherStudentAllocation.student_id == activity.student_id
    ).first()
    
    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to review this activity"
        )
    
    if activity.status.upper() != ActivityStatus.PENDING.value.upper():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity has already been reviewed"
        )
    
    # Teachers can now approve or reject activities
    if approval_data.status not in [ActivityStatus.APPROVED, ActivityStatus.REJECTED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be 'approved' or 'rejected'"
        )
    
    # Update activity status using raw SQL to avoid enum constraint issues
    status_value = approval_data.status.value.upper()  # Convert to uppercase for database
    db.execute(text("""
        UPDATE activities 
        SET status = :status, credits = :credits, updated_at = datetime('now')
        WHERE id = :activity_id
    """), {
        'status': status_value,
        'credits': approval_data.credits_awarded if approval_data.status == ActivityStatus.APPROVED else activity.credits,
        'activity_id': approval_data.activity_id
    })
    
    # Create approval record using raw SQL to avoid enum constraint issues
    
    approved_at = datetime.utcnow() if approval_data.status == ActivityStatus.APPROVED else None
    
    result = db.execute(text("""
        INSERT INTO activity_approvals (activity_id, teacher_id, status, comments, credits_awarded, approved_at, created_at)
        VALUES (:activity_id, :teacher_id, :status, :comments, :credits_awarded, :approved_at, datetime('now'))
        RETURNING id
    """), {
        'activity_id': approval_data.activity_id,
        'teacher_id': current_teacher.id,
        'status': approval_data.status.value.lower(),  # Convert to lowercase for database
        'comments': approval_data.comments,
        'credits_awarded': approval_data.credits_awarded or 0.0,
        'approved_at': approved_at
    })
    
    approval_id = result.fetchone()[0]
    db.commit()
    
    # Get the created approval for response
    approval_result = db.execute(text("""
        SELECT * FROM activity_approvals WHERE id = :id
    """), {'id': approval_id}).fetchone()
    
    # Create approval object for response
    approval = ActivityApproval(
        id=approval_result.id,
        activity_id=approval_result.activity_id,
        teacher_id=approval_result.teacher_id,
        status=ActivityStatus(approval_result.status),  # status is already lowercase
        comments=approval_result.comments,
        credits_awarded=approval_result.credits_awarded,
        approved_at=approval_result.approved_at,
        created_at=approval_result.created_at
    )
    
    # Log the approval/rejection
    from app.models.activity_log import ActivityLog, ActivityLogType
    log_type = ActivityLogType.ACTIVITY_APPROVED if approval_data.status == ActivityStatus.APPROVED else ActivityLogType.ACTIVITY_REJECTED
    log = ActivityLog(
        activity_id=approval_data.activity_id,
        user_id=current_teacher.id,
        log_type=log_type.value,  # Convert enum to string value
        action=f"Activity {approval_data.status.value} by teacher",
        details={
            "teacher_id": current_teacher.id,
            "teacher_name": current_teacher.full_name,
            "comments": approval_data.comments,
            "credits_awarded": approval_data.credits_awarded or 0.0
        }
    )
    db.add(log)
    
    # Update student's performance score and credits if approved
    if approval_data.status == ActivityStatus.APPROVED:
        # Update student's total credits and performance score
        db.execute(text("""
            UPDATE users 
            SET total_credits_earned = total_credits_earned + :credits,
                performance_score = performance_score + :credits
            WHERE id = :student_id
        """), {
            'credits': approval_data.credits_awarded or 0.0,
            'student_id': activity.student_id
        })
    
    db.commit()
    
    # Notify student about the decision
    from app.services.notification_service import NotificationService
    notification_service = NotificationService(db)
    notification_service.notify_student_of_activity_decision(
        activity_id=activity.id,
        student_id=activity.student_id,
        activity_title=activity.title,
        decision=approval_data.status.value,
        teacher_name=current_teacher.full_name,
        comments=approval_data.comments
    )
    
    # Return response with teacher name
    approval_response = ActivityApprovalResponse.from_orm(approval)
    approval_response.teacher_name = current_teacher.full_name
    
    return approval_response

@router.get("/approvals", response_model=List[dict])
def get_approval_history(
    current_teacher: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    """Get all approvals made by the current teacher with detailed information"""
    
    from sqlalchemy import text
    
    # Get detailed approval history with activity and student information
    result = db.execute(text("""
        SELECT 
            aa.id,
            aa.activity_id,
            aa.teacher_id,
            aa.status,
            aa.comments,
            aa.credits_awarded,
            aa.approved_at,
            aa.created_at,
            a.title as activity_title,
            a.description as activity_description,
            a.activity_type,
            a.credits as activity_credits,
            a.start_date,
            a.end_date,
            u.full_name as student_name,
            u.email as student_email,
            u.student_id,
            u.department as student_department
        FROM activity_approvals aa
        JOIN activities a ON aa.activity_id = a.id
        JOIN users u ON a.student_id = u.id
        WHERE aa.teacher_id = :teacher_id
        ORDER BY aa.created_at DESC
    """), {'teacher_id': current_teacher.id})
    
    approvals = []
    for row in result.fetchall():
        approval_data = {
            "id": row.id,
            "activity_id": row.activity_id,
            "teacher_id": row.teacher_id,
            "status": row.status,
            "comments": row.comments,
            "credits_awarded": row.credits_awarded,
            "approved_at": row.approved_at.isoformat() if row.approved_at else None,
            "created_at": row.created_at.isoformat(),
            "activity_title": row.activity_title,
            "activity_description": row.activity_description,
            "activity_type": row.activity_type,
            "activity_credits": row.activity_credits,
            "start_date": row.start_date.isoformat() if row.start_date else None,
            "end_date": row.end_date.isoformat() if row.end_date else None,
            "student_name": row.student_name,
            "student_email": row.student_email,
            "student_id": row.student_id,
            "student_department": row.student_department,
            "teacher_name": current_teacher.full_name
        }
        approvals.append(approval_data)
    
    return approvals

