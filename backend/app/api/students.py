from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime
from app.core.database import get_db
from app.core.auth import get_student_user
from app.models.user import User
from app.models.activity import Activity, ActivityType, ActivityStatus, StudentPerformance
from app.schemas.activity import (
    ActivityCreate, 
    ActivityResponse, 
    ActivityUpdate,
    StudentPerformanceResponse,
    DashboardStats
)

router = APIRouter(prefix="/students", tags=["students"])

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads/certificates"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/dashboard", response_model=DashboardStats)
def get_student_dashboard(
    current_student: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    """Get student dashboard statistics"""
    
    # Get activity statistics
    total_activities = db.query(Activity).filter(Activity.student_id == current_student.id).count()
    pending_activities = db.query(Activity).filter(
        Activity.student_id == current_student.id,
        Activity.status == ActivityStatus.PENDING
    ).count()
    approved_activities = db.query(Activity).filter(
        Activity.student_id == current_student.id,
        Activity.status == ActivityStatus.APPROVED
    ).count()
    rejected_activities = db.query(Activity).filter(
        Activity.student_id == current_student.id,
        Activity.status == ActivityStatus.REJECTED
    ).count()
    
    # Calculate total credits from approved activities
    total_credits_result = db.query(Activity).filter(
        Activity.student_id == current_student.id,
        Activity.status == ActivityStatus.APPROVED
    ).all()
    total_credits = sum(activity.credits or 0 for activity in total_credits_result)
    
    # Get latest performance data
    latest_performance = db.query(StudentPerformance).filter(
        StudentPerformance.student_id == current_student.id
    ).order_by(StudentPerformance.created_at.desc()).first()
    
    return DashboardStats(
        total_activities=total_activities,
        pending_activities=pending_activities,
        approved_activities=approved_activities,
        rejected_activities=rejected_activities,
        total_credits=total_credits,
        performance_score=current_student.performance_score or 0,
        total_credits_earned=current_student.total_credits_earned or 0,
        attendance_percentage=latest_performance.attendance_percentage if latest_performance else None,
        gpa=latest_performance.gpa if latest_performance else None
    )

@router.post("/activities", response_model=ActivityResponse)
async def create_activity(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    activity_type: ActivityType = Form(...),
    credits: Optional[float] = Form(0.0),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    certificate_file: Optional[UploadFile] = File(None),
    current_student: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    """Create a new activity submission"""
    
    try:
        print(f"🚀 Creating activity for student {current_student.id}")
        print(f"📝 Title: {title}")
        print(f"📝 Activity Type: {activity_type}")
        print(f"📝 Credits: {credits}")
        print(f"📝 Start Date: {start_date}")
        print(f"📝 End Date: {end_date}")
        
        # Parse dates
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date:
            try:
                parsed_start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                print(f"✅ Parsed start_date: {parsed_start_date}")
            except ValueError as e:
                print(f"❌ Failed to parse start_date '{start_date}': {e}")
                pass
        
        if end_date:
            try:
                parsed_end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                print(f"✅ Parsed end_date: {parsed_end_date}")
            except ValueError as e:
                print(f"❌ Failed to parse end_date '{end_date}': {e}")
                pass
        
        # Create activity
        activity = Activity(
            student_id=current_student.id,
            title=title,
            description=description,
            activity_type=activity_type,
            credits=credits,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            status=ActivityStatus.PENDING,
            files_count=0
        )
        
        db.add(activity)
        db.commit()
        db.refresh(activity)
        
        # Handle file upload if provided
        if certificate_file:
            from app.services.file_manager import file_manager
            try:
                file_storage = file_manager.save_file(certificate_file, activity.id, current_student.id, db)
                # Update activity with legacy file path for backward compatibility
                activity.certificate_file_path = file_storage.file_path
                db.commit()
            except Exception as e:
                # If file upload fails, still create the activity but log the error
                print(f"File upload failed: {e}")
        
        # Log activity creation (temporarily disabled due to enum issues)
        # from app.models.activity_log import ActivityLog, ActivityLogType
        # log = ActivityLog(
        #     activity_id=activity.id,
        #     user_id=current_student.id,
        #     log_type="activity_created",  # Use string value directly
        #     action=f"Activity '{title}' created",
        #     details={
        #         "activity_type": activity_type.value if hasattr(activity_type, 'value') else str(activity_type),
        #         "credits": credits,
        #         "has_file": certificate_file is not None
        #     }
        # )
        # db.add(log)
        
        # Notify assigned teachers about the new activity submission
        try:
            from app.services.notification_service import NotificationService
            notification_service = NotificationService(db)
            notification_service.notify_teachers_of_activity_submission(
                activity_id=activity.id,
                student_id=current_student.id,
                activity_title=title,
                student_name=current_student.full_name
            )
            print(f"✅ Notifications sent successfully")
        except Exception as e:
            print(f"⚠️ Failed to send notifications: {e}")
            # Don't fail the entire request if notifications fail
        
        db.commit()
        print(f"✅ Activity created successfully with ID: {activity.id}")
        
    except Exception as e:
        print(f"❌ Error creating activity: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create activity: {str(e)}"
        )
    
    # Add student name for response
    response_data = ActivityResponse.from_orm(activity)
    response_data.student_name = current_student.full_name
    
    return response_data

@router.get("/activities", response_model=List[ActivityResponse])
def get_student_activities(
    status: Optional[ActivityStatus] = None,
    current_student: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    """Get all activities for the current student"""
    
    query = db.query(Activity).filter(Activity.student_id == current_student.id)
    
    if status:
        query = query.filter(Activity.status == status)
    
    activities = query.order_by(Activity.created_at.desc()).all()
    
    # Add student name and files count to each activity
    response_activities = []
    for activity in activities:
        activity_data = ActivityResponse.from_orm(activity)
        activity_data.student_name = current_student.full_name
        
        # Get files count
        from app.models.activity_log import FileStorage
        files_count = db.query(FileStorage).filter(FileStorage.activity_id == activity.id).count()
        activity_data.files_count = files_count
        
        response_activities.append(activity_data)
    
    return response_activities

@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: int,
    current_student: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    """Get a specific activity"""
    
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.student_id == current_student.id
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    response_data = ActivityResponse.from_orm(activity)
    response_data.student_name = current_student.full_name
    
    return response_data

@router.put("/activities/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    activity_type: Optional[ActivityType] = Form(None),
    credits: Optional[float] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    certificate_file: Optional[UploadFile] = File(None),
    current_student: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    """Update an activity (only if it's pending)"""
    
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.student_id == current_student.id
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    if activity.status != ActivityStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update activity that has been reviewed"
        )
    
    # Update fields
    if title is not None:
        activity.title = title
    if description is not None:
        activity.description = description
    if activity_type is not None:
        activity.activity_type = activity_type
    if credits is not None:
        activity.credits = credits
    
    # Handle date updates
    if start_date is not None:
        try:
            activity.start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except ValueError:
            pass
    
    if end_date is not None:
        try:
            activity.end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except ValueError:
            pass
    
    # Handle file upload
    if certificate_file:
        # Delete old file if exists
        if activity.certificate_file_path and os.path.exists(activity.certificate_file_path):
            os.remove(activity.certificate_file_path)
        
        # Save new file
        file_extension = os.path.splitext(certificate_file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        certificate_file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(certificate_file_path, "wb") as buffer:
            content = await certificate_file.read()
            buffer.write(content)
        
        activity.certificate_file_path = certificate_file_path
    
    db.commit()
    db.refresh(activity)
    
    response_data = ActivityResponse.from_orm(activity)
    response_data.student_name = current_student.full_name
    
    return response_data

@router.delete("/activities/{activity_id}")
def delete_activity(
    activity_id: int,
    current_student: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    """Delete an activity (only if it's pending)"""
    
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.student_id == current_student.id
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    if activity.status != ActivityStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete activity that has been reviewed"
        )
    
    # Delete associated file
    if activity.certificate_file_path and os.path.exists(activity.certificate_file_path):
        os.remove(activity.certificate_file_path)
    
    db.delete(activity)
    db.commit()
    
    return {"message": "Activity deleted successfully"}

@router.get("/performance", response_model=List[StudentPerformanceResponse])
def get_student_performance(
    current_student: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    """Get student performance history"""
    
    performance_records = db.query(StudentPerformance).filter(
        StudentPerformance.student_id == current_student.id
    ).order_by(StudentPerformance.created_at.desc()).all()
    
    return performance_records

