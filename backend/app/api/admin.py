from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import csv
import io
from datetime import datetime
from app.core.database import get_db
from app.core.auth import get_admin_user
from app.models.user import User, UserRole, UserStatus, TeacherStudentAllocation
from app.schemas.user import (
    UserResponse, 
    UserApproval, 
    TeacherStudentAllocationCreate,
    TeacherStudentAllocationResponse
)
from fast_auth_service import fast_auth
from app.services.erp_integration_service import erp_service

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    role: Optional[UserRole] = Query(None),
    status: Optional[UserStatus] = Query(None),
    current_admin: User = Depends(get_admin_user)
):
    """Get all users with fast local database access"""
    try:
        # Get users from fast auth service
        users_data = fast_auth.get_users()
        
        # Filter by role if specified
        if role:
            role_str = role.value.lower() if hasattr(role, 'value') else str(role).lower()
            users_data = [user for user in users_data if user.get('role') == role_str]
        
        # Filter by status if specified
        if status:
            status_str = status.value.lower() if hasattr(status, 'value') else str(status).lower()
            users_data = [user for user in users_data if user.get('status') == status_str]
        
        # Convert to User objects
        users = []
        for user_data in users_data:
            user = User(
                id=user_data["id"],
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                hashed_password=None,  # Don't return hashed password
                role=user_data["role"],
                status=user_data["status"],
                is_active=user_data["is_active"],
                phone_number=user_data["phone_number"],
                department=user_data["department"],
                student_id=user_data["student_id"],
                employee_id=user_data["employee_id"],
                performance_score=user_data["performance_score"] or 0,
                total_credits_earned=user_data["total_credits_earned"] or 0,
                profile_picture=user_data["profile_picture"],
                bio=user_data["bio"],
                date_of_birth=user_data["date_of_birth"],
                address=user_data["address"],
                city=user_data["city"],
                state=user_data["state"],
                country=user_data["country"],
                postal_code=user_data["postal_code"],
                linkedin_url=user_data["linkedin_url"],
                twitter_url=user_data["twitter_url"],
                website_url=user_data["website_url"],
                is_oauth_user=user_data["is_oauth_user"] or False,
                verification_code=user_data["verification_code"],
                verification_expires=user_data["verification_expires"],
                created_at=user_data["created_at"],
                updated_at=user_data["updated_at"]
            )
            users.append(user)
        
        return users
        
    except Exception as e:
        print(f"Error getting users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )

@router.get("/database-stats")
def get_database_stats(current_admin: User = Depends(get_admin_user)):
    """Get real-time database statistics"""
    try:
        stats = fast_auth.get_database_stats()
        return stats
    except Exception as e:
        print(f"Error getting database stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve database statistics"
        )

@router.post("/sync-supabase")
def sync_with_supabase(current_admin: User = Depends(get_admin_user)):
    """Manually sync with Supabase"""
    try:
        success = hybrid_db.sync_with_supabase()
        if success:
            return {"message": "Successfully synced with Supabase", "status": "success"}
        else:
            return {"message": "Sync failed - check Supabase connection", "status": "error"}
    except Exception as e:
        print(f"Error syncing with Supabase: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync with Supabase"
        )

@router.get("/pending-users", response_model=List[UserResponse])
def get_pending_users(
    role: Optional[UserRole] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """Get all pending user registrations"""
    from sqlalchemy import text
    
    # Use raw SQL to avoid enum issues
    if role:
        role_str = role.value.lower() if hasattr(role, 'value') else str(role).lower()
        result = db.execute(text("""
            SELECT id, email, username, full_name, role, status, is_active, phone_number, 
                   department, student_id, employee_id, created_at, updated_at
            FROM users 
            WHERE status = 'PENDING' AND role = :role
            ORDER BY created_at DESC
        """), {"role": role_str.upper()})
    else:
        result = db.execute(text("""
            SELECT id, email, username, full_name, role, status, is_active, phone_number, 
                   department, student_id, employee_id, created_at, updated_at
            FROM users 
            WHERE status = 'PENDING'
            ORDER BY created_at DESC
        """))
    
    users = []
    for row in result.fetchall():
        user = User(
            id=row.id,
            email=row.email,
            username=row.username,
            full_name=row.full_name,
            hashed_password="",  # Don't return password
            role=row.role.lower(),  # Convert to lowercase for enum compatibility
            status=row.status.lower(),  # Convert to lowercase for enum compatibility
            is_active=row.is_active,
            phone_number=row.phone_number,
            department=row.department,
            student_id=row.student_id,
            employee_id=row.employee_id,
            created_at=row.created_at,
            updated_at=row.updated_at
        )
        users.append(user)
    
    return users

@router.post("/approve-user")
def approve_user(
    approval_data: UserApproval,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """Approve or reject a user registration"""
    
    # Use raw SQL to avoid enum issues
    from sqlalchemy import text
    result = db.execute(text("SELECT * FROM users WHERE id = :user_id"), 
                      {"user_id": approval_data.user_id}).fetchone()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if result.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in pending status"
        )
    
    # Update user status using raw SQL
    db.execute(text("""
        UPDATE users 
        SET status = :status, updated_at = datetime('now') 
        WHERE id = :user_id
    """), {
        "status": approval_data.status.value.upper(),
        "user_id": approval_data.user_id
    })
    db.commit()
    
    return {
        "message": f"User {approval_data.status} successfully",
        "user_id": approval_data.user_id,
        "status": approval_data.status
    }


@router.get("/teachers", response_model=List[UserResponse])
def get_approved_teachers(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """Get all approved teachers"""
    return db.query(User).filter(
        User.role == UserRole.TEACHER,
        User.status == UserStatus.APPROVED
    ).all()

@router.get("/students", response_model=List[UserResponse])
def get_approved_students(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """Get all approved students"""
    return db.query(User).filter(
        User.role == UserRole.STUDENT,
        User.status == UserStatus.APPROVED
    ).all()

@router.post("/allocate-students")
def allocate_students_to_teacher(
    allocation_data: TeacherStudentAllocationCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """Allocate multiple students to a teacher"""
    
    # Verify teacher exists and is approved
    teacher = db.query(User).filter(
        User.id == allocation_data.teacher_id,
        User.role == UserRole.TEACHER,
        User.status == UserStatus.APPROVED
    ).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found or not approved"
        )
    
    # Verify all students exist and are approved
    students = db.query(User).filter(
        User.id.in_(allocation_data.student_ids),
        User.role == UserRole.STUDENT,
        User.status == UserStatus.APPROVED
    ).all()
    
    if len(students) != len(allocation_data.student_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more students not found or not approved"
        )
    
    # Create allocations
    allocations_created = []
    for student_id in allocation_data.student_ids:
        # Check if allocation already exists
        existing_allocation = db.query(TeacherStudentAllocation).filter(
            TeacherStudentAllocation.teacher_id == allocation_data.teacher_id,
            TeacherStudentAllocation.student_id == student_id
        ).first()
        
        if not existing_allocation:
            allocation = TeacherStudentAllocation(
                teacher_id=allocation_data.teacher_id,
                student_id=student_id,
                allocated_by=current_admin.id
            )
            db.add(allocation)
            allocations_created.append(student_id)
    
    db.commit()
    
    # Sync to Supabase
    try:
        from app.core.supabase_client import get_supabase_client
        supabase = get_supabase_client()
        
        # Get the created allocations for Supabase sync
        created_allocations = db.query(TeacherStudentAllocation).filter(
            TeacherStudentAllocation.teacher_id == allocation_data.teacher_id,
            TeacherStudentAllocation.student_id.in_(allocations_created)
        ).all()
        
        # Prepare data for Supabase
        supabase_data = []
        for allocation in created_allocations:
            supabase_data.append({
                "id": allocation.id,
                "teacher_id": allocation.teacher_id,
                "student_id": allocation.student_id,
                "allocated_by": allocation.allocated_by,
                "created_at": allocation.created_at.isoformat() if allocation.created_at else None
            })
        
        if supabase_data:
            # Insert into Supabase
            result = supabase.table("teacher_student_allocations").insert(supabase_data).execute()
            print(f"✅ Synced {len(supabase_data)} allocations to Supabase")
            
    except Exception as e:
        print(f"⚠️ Failed to sync allocations to Supabase: {e}")
        # Don't fail the request if Supabase sync fails
    
    return {
        "message": f"Successfully allocated {len(allocations_created)} students to teacher",
        "teacher_id": allocation_data.teacher_id,
        "allocated_students": allocations_created
    }

@router.get("/allocations", response_model=List[TeacherStudentAllocationResponse])
def get_all_allocations(
    teacher_id: Optional[int] = Query(None),
    student_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """Get all teacher-student allocations"""
    query = db.query(
        TeacherStudentAllocation.id,
        TeacherStudentAllocation.teacher_id,
        TeacherStudentAllocation.student_id,
        TeacherStudentAllocation.created_at,
        User.full_name.label("teacher_name")
    ).join(
        User, User.id == TeacherStudentAllocation.teacher_id
    )
    
    if teacher_id:
        query = query.filter(TeacherStudentAllocation.teacher_id == teacher_id)
    
    if student_id:
        query = query.filter(TeacherStudentAllocation.student_id == student_id)
    
    results = query.all()
    
    # Get student names
    allocations = []
    for result in results:
        student = db.query(User).filter(User.id == result.student_id).first()
        allocation_data = {
            "id": result.id,
            "teacher_id": result.teacher_id,
            "student_id": result.student_id,
            "teacher_name": result.teacher_name,
            "student_name": student.full_name if student else "Unknown",
            "created_at": result.created_at
        }
        allocations.append(TeacherStudentAllocationResponse(**allocation_data))
    
    return allocations

@router.delete("/allocations/{allocation_id}")
def remove_allocation(
    allocation_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """Remove a teacher-student allocation"""
    
    allocation = db.query(TeacherStudentAllocation).filter(
        TeacherStudentAllocation.id == allocation_id
    ).first()
    
    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allocation not found"
        )
    
    db.delete(allocation)
    db.commit()
    
    return {"message": "Allocation removed successfully"}

# Activity approval is now handled by teachers, not admins

@router.get("/activities/pending", response_model=List[dict])
def get_pending_activities(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """Get all pending activities for admin review"""
    
    from app.models.activity import Activity, ActivityStatus
    from app.models.user import User
    from app.models.activity_log import FileStorage
    
    activities = db.query(Activity).filter(
        Activity.status == ActivityStatus.PENDING
    ).order_by(Activity.created_at.desc()).all()
    
    result = []
    for activity in activities:
        # Get student info
        student = db.query(User).filter(User.id == activity.student_id).first()
        
        # Get files count
        files_count = db.query(FileStorage).filter(FileStorage.activity_id == activity.id).count()
        
        activity_data = {
            "id": activity.id,
            "student_id": activity.student_id,
            "student_name": student.full_name if student else "Unknown",
            "student_email": student.email if student else "Unknown",
            "title": activity.title,
            "description": activity.description,
            "activity_type": activity.activity_type.value if hasattr(activity.activity_type, 'value') else str(activity.activity_type),
            "credits": activity.credits,
            "start_date": activity.start_date.isoformat() if activity.start_date else None,
            "end_date": activity.end_date.isoformat() if activity.end_date else None,
            "status": activity.status.value if hasattr(activity.status, 'value') else str(activity.status),
            "files_count": files_count,
            "created_at": activity.created_at.isoformat(),
            "updated_at": activity.updated_at.isoformat() if activity.updated_at else None
        }
        result.append(activity_data)
    
    return result

@router.get("/activities/all", response_model=List[dict])
def get_all_activities(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """Get all activities for admin overview"""
    
    from app.models.activity import Activity, ActivityStatus
    from app.models.user import User
    from app.models.activity_log import FileStorage
    
    activities = db.query(Activity).order_by(Activity.created_at.desc()).all()
    
    result = []
    for activity in activities:
        # Get student info
        student = db.query(User).filter(User.id == activity.student_id).first()
        
        # Get files count
        files_count = db.query(FileStorage).filter(FileStorage.activity_id == activity.id).count()
        
        activity_data = {
            "id": activity.id,
            "student_id": activity.student_id,
            "student_name": student.full_name if student else "Unknown",
            "student_email": student.email if student else "Unknown",
            "title": activity.title,
            "description": activity.description,
            "activity_type": activity.activity_type.value if hasattr(activity.activity_type, 'value') else str(activity.activity_type),
            "credits": activity.credits,
            "start_date": activity.start_date.isoformat() if activity.start_date else None,
            "end_date": activity.end_date.isoformat() if activity.end_date else None,
            "status": activity.status.value if hasattr(activity.status, 'value') else str(activity.status),
            "files_count": files_count,
            "created_at": activity.created_at.isoformat(),
            "updated_at": activity.updated_at.isoformat() if activity.updated_at else None
        }
        result.append(activity_data)
    
    return result
