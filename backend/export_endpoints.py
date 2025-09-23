from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
import csv
import io
from datetime import datetime
from app.core.database import get_db
from app.core.auth import get_admin_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/export/teachers")
def export_teachers_data(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Export all teachers data to CSV"""
    try:
        # Get all teachers with their allocations
        teachers_query = text("""
            SELECT 
                u.id, u.email, u.username, u.full_name, u.phone_number, 
                u.department, u.employee_id, u.performance_score, 
                u.total_credits_earned, u.created_at, u.updated_at,
                COUNT(tsa.student_id) as assigned_students_count
            FROM users u
            LEFT JOIN teacher_student_allocations tsa ON u.id = tsa.teacher_id
            WHERE u.role = 'TEACHER'
            GROUP BY u.id
            ORDER BY u.created_at DESC
        """)
        
        teachers_result = db.execute(teachers_query).fetchall()
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Email', 'Username', 'Full Name', 'Phone Number', 
            'Department', 'Employee ID', 'Performance Score', 
            'Total Credits Earned', 'Assigned Students Count', 
            'Created At', 'Updated At'
        ])
        
        # Write data
        for teacher in teachers_result:
            writer.writerow([
                teacher.id,
                teacher.email,
                teacher.username,
                teacher.full_name,
                teacher.phone_number,
                teacher.department,
                teacher.employee_id,
                teacher.performance_score,
                teacher.total_credits_earned,
                teacher.assigned_students_count,
                teacher.created_at.isoformat() if teacher.created_at else '',
                teacher.updated_at.isoformat() if teacher.updated_at else ''
            ])
        
        output.seek(0)
        
        # Create response
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=teachers_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export teachers data: {str(e)}"
        )

@router.get("/export/students")
def export_students_data(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Export all students data to CSV"""
    try:
        # Get all students with their activities and allocations
        students_query = text("""
            SELECT 
                u.id, u.email, u.username, u.full_name, u.phone_number, 
                u.department, u.student_id, u.performance_score, 
                u.total_credits_earned, u.created_at, u.updated_at,
                COUNT(DISTINCT a.id) as total_activities,
                COUNT(DISTINCT CASE WHEN a.status = 'APPROVED' THEN a.id END) as approved_activities,
                COUNT(DISTINCT CASE WHEN a.status = 'PENDING' THEN a.id END) as pending_activities,
                COUNT(DISTINCT CASE WHEN a.status = 'REJECTED' THEN a.id END) as rejected_activities,
                COALESCE(SUM(a.credits), 0) as total_credits_earned_from_activities
            FROM users u
            LEFT JOIN activities a ON u.id = a.user_id
            WHERE u.role = 'STUDENT'
            GROUP BY u.id
            ORDER BY u.created_at DESC
        """)
        
        students_result = db.execute(students_query).fetchall()
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Email', 'Username', 'Full Name', 'Phone Number', 
            'Department', 'Student ID', 'Performance Score', 
            'Total Credits Earned', 'Total Activities', 
            'Approved Activities', 'Pending Activities', 'Rejected Activities',
            'Credits from Activities', 'Created At', 'Updated At'
        ])
        
        # Write data
        for student in students_result:
            writer.writerow([
                student.id,
                student.email,
                student.username,
                student.full_name,
                student.phone_number,
                student.department,
                student.student_id,
                student.performance_score,
                student.total_credits_earned,
                student.total_activities,
                student.approved_activities,
                student.pending_activities,
                student.rejected_activities,
                student.total_credits_earned_from_activities,
                student.created_at.isoformat() if student.created_at else '',
                student.updated_at.isoformat() if student.updated_at else ''
            ])
        
        output.seek(0)
        
        # Create response
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=students_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export students data: {str(e)}"
        )

@router.get("/export/comprehensive")
def export_comprehensive_data(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Export comprehensive data including users, activities, and allocations"""
    try:
        # Get comprehensive data
        comprehensive_query = text("""
            SELECT 
                'USER' as data_type,
                u.id, u.email, u.username, u.full_name, u.role, u.status,
                u.phone_number, u.department, u.student_id, u.employee_id,
                u.performance_score, u.total_credits_earned, u.created_at, u.updated_at,
                NULL as activity_title, NULL as activity_type, NULL as activity_status,
                NULL as activity_credits, NULL as teacher_name, NULL as allocated_by_name
            FROM users u
            
            UNION ALL
            
            SELECT 
                'ACTIVITY' as data_type,
                a.id, u.email, u.username, u.full_name, u.role, u.status,
                u.phone_number, u.department, u.student_id, u.employee_id,
                u.performance_score, u.total_credits_earned, u.created_at, u.updated_at,
                a.title as activity_title, a.activity_type, a.status as activity_status,
                a.credits as activity_credits, NULL as teacher_name, NULL as allocated_by_name
            FROM activities a
            JOIN users u ON a.user_id = u.id
            
            UNION ALL
            
            SELECT 
                'ALLOCATION' as data_type,
                tsa.id, s.email, s.username, s.full_name, s.role, s.status,
                s.phone_number, s.department, s.student_id, s.employee_id,
                s.performance_score, s.total_credits_earned, s.created_at, s.updated_at,
                NULL as activity_title, NULL as activity_type, NULL as activity_status,
                NULL as activity_credits, t.full_name as teacher_name, admin.full_name as allocated_by_name
            FROM teacher_student_allocations tsa
            JOIN users s ON tsa.student_id = s.id
            JOIN users t ON tsa.teacher_id = t.id
            LEFT JOIN users admin ON tsa.allocated_by = admin.id
            
            ORDER BY data_type, created_at DESC
        """)
        
        comprehensive_result = db.execute(comprehensive_query).fetchall()
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Data Type', 'ID', 'Email', 'Username', 'Full Name', 'Role', 'Status',
            'Phone Number', 'Department', 'Student ID', 'Employee ID',
            'Performance Score', 'Total Credits Earned', 'Created At', 'Updated At',
            'Activity Title', 'Activity Type', 'Activity Status', 'Activity Credits',
            'Teacher Name', 'Allocated By'
        ])
        
        # Write data
        for row in comprehensive_result:
            writer.writerow([
                row.data_type,
                row.id,
                row.email,
                row.username,
                row.full_name,
                row.role,
                row.status,
                row.phone_number,
                row.department,
                row.student_id,
                row.employee_id,
                row.performance_score,
                row.total_credits_earned,
                row.created_at.isoformat() if row.created_at else '',
                row.updated_at.isoformat() if row.updated_at else '',
                row.activity_title,
                row.activity_type,
                row.activity_status,
                row.activity_credits,
                row.teacher_name,
                row.allocated_by_name
            ])
        
        output.seek(0)
        
        # Create response
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=comprehensive_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export comprehensive data: {str(e)}"
        )

