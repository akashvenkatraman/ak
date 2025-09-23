from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
import csv
import io
import json
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.auth import get_admin_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Analytics"])

@router.get("/export/teachers-performance")
def export_teachers_performance_data(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Export teachers performance data with activity metrics for NIRF/AICTE reporting"""
    try:
        # Get comprehensive teachers performance data
        teachers_query = text("""
            SELECT 
                u.id, u.email, u.username, u.full_name, u.phone_number, 
                u.department, u.employee_id, u.performance_score, 
                u.total_credits_earned, u.created_at, u.updated_at,
                COUNT(DISTINCT tsa.student_id) as assigned_students_count,
                COUNT(DISTINCT a.id) as total_activities_reviewed,
                COUNT(DISTINCT CASE WHEN a.status = 'APPROVED' THEN a.id END) as approved_activities,
                COUNT(DISTINCT CASE WHEN a.status = 'REJECTED' THEN a.id END) as rejected_activities,
                COUNT(DISTINCT CASE WHEN a.status = 'PENDING' THEN a.id END) as pending_activities,
                COALESCE(SUM(a.credits), 0) as total_credits_awarded,
                COALESCE(AVG(a.credits), 0) as average_credits_per_activity,
                COUNT(DISTINCT CASE WHEN a.created_at >= date('now', '-30 days') THEN a.id END) as activities_last_30_days,
                COUNT(DISTINCT CASE WHEN a.created_at >= date('now', '-90 days') THEN a.id END) as activities_last_90_days,
                COUNT(DISTINCT CASE WHEN a.created_at >= date('now', '-365 days') THEN a.id END) as activities_last_year
            FROM users u
            LEFT JOIN teacher_student_allocations tsa ON u.id = tsa.teacher_id
            LEFT JOIN activities a ON tsa.student_id = a.user_id
            WHERE u.role = 'TEACHER'
            GROUP BY u.id
            ORDER BY u.total_credits_earned DESC, u.performance_score DESC
        """)
        
        teachers_result = db.execute(teachers_query).fetchall()
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header with performance metrics
        writer.writerow([
            'Teacher ID', 'Email', 'Full Name', 'Department', 'Employee ID',
            'Performance Score', 'Total Credits Earned', 'Assigned Students',
            'Total Activities Reviewed', 'Approved Activities', 'Rejected Activities', 'Pending Activities',
            'Total Credits Awarded', 'Average Credits per Activity',
            'Activities (Last 30 Days)', 'Activities (Last 90 Days)', 'Activities (Last Year)',
            'Approval Rate (%)', 'Rejection Rate (%)', 'Activity Review Efficiency',
            'Created At', 'Last Updated'
        ])
        
        # Write data with calculated metrics
        for teacher in teachers_result:
            total_reviewed = teacher.total_activities_reviewed or 0
            approved = teacher.approved_activities or 0
            rejected = teacher.rejected_activities or 0
            
            approval_rate = (approved / total_reviewed * 100) if total_reviewed > 0 else 0
            rejection_rate = (rejected / total_reviewed * 100) if total_reviewed > 0 else 0
            efficiency = (total_reviewed / (teacher.assigned_students_count or 1)) if teacher.assigned_students_count > 0 else 0
            
            writer.writerow([
                teacher.id,
                teacher.email,
                teacher.full_name,
                teacher.department,
                teacher.employee_id,
                teacher.performance_score,
                teacher.total_credits_earned,
                teacher.assigned_students_count,
                total_reviewed,
                approved,
                rejected,
                teacher.pending_activities,
                teacher.total_credits_awarded,
                round(teacher.average_credits_per_activity, 2),
                teacher.activities_last_30_days,
                teacher.activities_last_90_days,
                teacher.activities_last_year,
                round(approval_rate, 2),
                round(rejection_rate, 2),
                round(efficiency, 2),
                teacher.created_at.isoformat() if teacher.created_at else '',
                teacher.updated_at.isoformat() if teacher.updated_at else ''
            ])
        
        output.seek(0)
        
        # Create response
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=teachers_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export teachers performance data: {str(e)}"
        )

@router.get("/export/students-performance")
def export_students_performance_data(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Export students performance data with activity metrics for NIRF/AICTE reporting"""
    try:
        # Get comprehensive students performance data
        students_query = text("""
            SELECT 
                u.id, u.email, u.username, u.full_name, u.phone_number, 
                u.department, u.student_id, u.performance_score, 
                u.total_credits_earned, u.created_at, u.updated_at,
                COUNT(DISTINCT a.id) as total_activities,
                COUNT(DISTINCT CASE WHEN a.status = 'APPROVED' THEN a.id END) as approved_activities,
                COUNT(DISTINCT CASE WHEN a.status = 'REJECTED' THEN a.id END) as rejected_activities,
                COUNT(DISTINCT CASE WHEN a.status = 'PENDING' THEN a.id END) as pending_activities,
                COALESCE(SUM(a.credits), 0) as total_credits_earned_from_activities,
                COALESCE(AVG(a.credits), 0) as average_credits_per_activity,
                COUNT(DISTINCT CASE WHEN a.created_at >= date('now', '-30 days') THEN a.id END) as activities_last_30_days,
                COUNT(DISTINCT CASE WHEN a.created_at >= date('now', '-90 days') THEN a.id END) as activities_last_90_days,
                COUNT(DISTINCT CASE WHEN a.created_at >= date('now', '-365 days') THEN a.id END) as activities_last_year,
                COUNT(DISTINCT CASE WHEN a.activity_type = 'CERTIFICATE' THEN a.id END) as certificate_activities,
                COUNT(DISTINCT CASE WHEN a.activity_type = 'PROJECT' THEN a.id END) as project_activities,
                COUNT(DISTINCT CASE WHEN a.activity_type = 'INTERNSHIP' THEN a.id END) as internship_activities,
                COUNT(DISTINCT CASE WHEN a.activity_type = 'RESEARCH' THEN a.id END) as research_activities,
                COUNT(DISTINCT CASE WHEN a.activity_type = 'SEMINAR' THEN a.id END) as seminar_activities,
                COUNT(DISTINCT CASE WHEN a.activity_type = 'WORKSHOP' THEN a.id END) as workshop_activities,
                t.full_name as assigned_teacher,
                tsa.created_at as allocation_date
            FROM users u
            LEFT JOIN activities a ON u.id = a.user_id
            LEFT JOIN teacher_student_allocations tsa ON u.id = tsa.student_id
            LEFT JOIN users t ON tsa.teacher_id = t.id
            WHERE u.role = 'STUDENT'
            GROUP BY u.id
            ORDER BY u.total_credits_earned DESC, u.performance_score DESC
        """)
        
        students_result = db.execute(students_query).fetchall()
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header with performance metrics
        writer.writerow([
            'Student ID', 'Email', 'Full Name', 'Department', 'Student ID Number',
            'Performance Score', 'Total Credits Earned', 'Assigned Teacher',
            'Total Activities', 'Approved Activities', 'Rejected Activities', 'Pending Activities',
            'Total Credits from Activities', 'Average Credits per Activity',
            'Activities (Last 30 Days)', 'Activities (Last 90 Days)', 'Activities (Last Year)',
            'Certificate Activities', 'Project Activities', 'Internship Activities',
            'Research Activities', 'Seminar Activities', 'Workshop Activities',
            'Success Rate (%)', 'Activity Completion Rate (%)', 'Credits per Month',
            'Allocation Date', 'Created At', 'Last Updated'
        ])
        
        # Write data with calculated metrics
        for student in students_result:
            total_activities = student.total_activities or 0
            approved = student.approved_activities or 0
            rejected = student.rejected_activities or 0
            
            success_rate = (approved / total_activities * 100) if total_activities > 0 else 0
            completion_rate = ((approved + rejected) / total_activities * 100) if total_activities > 0 else 0
            
            # Calculate credits per month (based on last 12 months)
            months_since_creation = max(1, (datetime.now() - (student.created_at or datetime.now())).days / 30)
            credits_per_month = (student.total_credits_earned_from_activities or 0) / months_since_creation
            
            writer.writerow([
                student.id,
                student.email,
                student.full_name,
                student.department,
                student.student_id,
                student.performance_score,
                student.total_credits_earned,
                student.assigned_teacher or 'Not Assigned',
                total_activities,
                approved,
                rejected,
                student.pending_activities,
                student.total_credits_earned_from_activities,
                round(student.average_credits_per_activity, 2),
                student.activities_last_30_days,
                student.activities_last_90_days,
                student.activities_last_year,
                student.certificate_activities,
                student.project_activities,
                student.internship_activities,
                student.research_activities,
                student.seminar_activities,
                student.workshop_activities,
                round(success_rate, 2),
                round(completion_rate, 2),
                round(credits_per_month, 2),
                student.allocation_date.isoformat() if student.allocation_date else '',
                student.created_at.isoformat() if student.created_at else '',
                student.updated_at.isoformat() if student.updated_at else ''
            ])
        
        output.seek(0)
        
        # Create response
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=students_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export students performance data: {str(e)}"
        )

@router.get("/export/nirf-metrics")
def export_nirf_metrics(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Export NIRF/AICTE specific metrics for institutional reporting"""
    try:
        # Get NIRF metrics
        nirf_query = text("""
            WITH department_stats AS (
                SELECT 
                    u.department,
                    COUNT(DISTINCT u.id) as total_students,
                    COUNT(DISTINCT CASE WHEN u.role = 'TEACHER' THEN u.id END) as total_teachers,
                    COUNT(DISTINCT a.id) as total_activities,
                    COUNT(DISTINCT CASE WHEN a.status = 'APPROVED' THEN a.id END) as approved_activities,
                    COALESCE(SUM(a.credits), 0) as total_credits,
                    COALESCE(AVG(a.credits), 0) as avg_credits_per_activity,
                    COUNT(DISTINCT CASE WHEN a.activity_type = 'RESEARCH' THEN a.id END) as research_activities,
                    COUNT(DISTINCT CASE WHEN a.activity_type = 'PROJECT' THEN a.id END) as project_activities,
                    COUNT(DISTINCT CASE WHEN a.activity_type = 'INTERNSHIP' THEN a.id END) as internship_activities
                FROM users u
                LEFT JOIN activities a ON u.id = a.user_id
                WHERE u.role IN ('STUDENT', 'TEACHER')
                GROUP BY u.department
            ),
            overall_stats AS (
                SELECT 
                    COUNT(DISTINCT CASE WHEN u.role = 'STUDENT' THEN u.id END) as total_students,
                    COUNT(DISTINCT CASE WHEN u.role = 'TEACHER' THEN u.id END) as total_teachers,
                    COUNT(DISTINCT a.id) as total_activities,
                    COUNT(DISTINCT CASE WHEN a.status = 'APPROVED' THEN a.id END) as approved_activities,
                    COALESCE(SUM(a.credits), 0) as total_credits,
                    COALESCE(AVG(a.credits), 0) as avg_credits_per_activity,
                    COUNT(DISTINCT CASE WHEN a.activity_type = 'RESEARCH' THEN a.id END) as research_activities,
                    COUNT(DISTINCT CASE WHEN a.activity_type = 'PROJECT' THEN a.id END) as project_activities,
                    COUNT(DISTINCT CASE WHEN a.activity_type = 'INTERNSHIP' THEN a.id END) as internship_activities,
                    COUNT(DISTINCT u.department) as total_departments
                FROM users u
                LEFT JOIN activities a ON u.id = a.user_id
                WHERE u.role IN ('STUDENT', 'TEACHER')
            )
            SELECT 
                'OVERALL' as department,
                os.total_students,
                os.total_teachers,
                os.total_activities,
                os.approved_activities,
                os.total_credits,
                os.avg_credits_per_activity,
                os.research_activities,
                os.project_activities,
                os.internship_activities,
                os.total_departments,
                CASE WHEN os.total_students > 0 THEN ROUND(os.total_teachers * 100.0 / os.total_students, 2) ELSE 0 END as student_teacher_ratio,
                CASE WHEN os.total_activities > 0 THEN ROUND(os.approved_activities * 100.0 / os.total_activities, 2) ELSE 0 END as activity_approval_rate,
                CASE WHEN os.total_students > 0 THEN ROUND(os.total_activities * 1.0 / os.total_students, 2) ELSE 0 END as activities_per_student
            FROM overall_stats os
            
            UNION ALL
            
            SELECT 
                ds.department,
                ds.total_students,
                ds.total_teachers,
                ds.total_activities,
                ds.approved_activities,
                ds.total_credits,
                ds.avg_credits_per_activity,
                ds.research_activities,
                ds.project_activities,
                ds.internship_activities,
                1 as total_departments,
                CASE WHEN ds.total_students > 0 THEN ROUND(ds.total_teachers * 100.0 / ds.total_students, 2) ELSE 0 END as student_teacher_ratio,
                CASE WHEN ds.total_activities > 0 THEN ROUND(ds.approved_activities * 100.0 / ds.total_activities, 2) ELSE 0 END as activity_approval_rate,
                CASE WHEN ds.total_students > 0 THEN ROUND(ds.total_activities * 1.0 / ds.total_students, 2) ELSE 0 END as activities_per_student
            FROM department_stats ds
            
            ORDER BY department
        """)
        
        nirf_result = db.execute(nirf_query).fetchall()
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Department', 'Total Students', 'Total Teachers', 'Total Activities',
            'Approved Activities', 'Total Credits', 'Average Credits per Activity',
            'Research Activities', 'Project Activities', 'Internship Activities',
            'Total Departments', 'Student-Teacher Ratio (%)', 'Activity Approval Rate (%)',
            'Activities per Student', 'Research Intensity (%)', 'Project Intensity (%)',
            'Internship Intensity (%)', 'Overall Performance Score'
        ])
        
        # Write data
        for row in nirf_result:
            total_activities = row.total_activities or 0
            research_intensity = (row.research_activities / total_activities * 100) if total_activities > 0 else 0
            project_intensity = (row.project_activities / total_activities * 100) if total_activities > 0 else 0
            internship_intensity = (row.internship_activities / total_activities * 100) if total_activities > 0 else 0
            
            # Calculate overall performance score (weighted average)
            performance_score = (
                (row.activity_approval_rate or 0) * 0.3 +
                (row.activities_per_student or 0) * 0.2 +
                (research_intensity) * 0.2 +
                (project_intensity) * 0.15 +
                (internship_intensity) * 0.15
            )
            
            writer.writerow([
                row.department,
                row.total_students,
                row.total_teachers,
                total_activities,
                row.approved_activities,
                row.total_credits,
                round(row.avg_credits_per_activity, 2),
                row.research_activities,
                row.project_activities,
                row.internship_activities,
                row.total_departments,
                round(row.student_teacher_ratio, 2),
                round(row.activity_approval_rate, 2),
                round(row.activities_per_student, 2),
                round(research_intensity, 2),
                round(project_intensity, 2),
                round(internship_intensity, 2),
                round(performance_score, 2)
            ])
        
        output.seek(0)
        
        # Create response
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=nirf_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export NIRF metrics: {str(e)}"
        )

@router.get("/analytics/dashboard-data")
def get_analytics_dashboard_data(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get data for analytics dashboard with charts and metrics"""
    try:
        # Get comprehensive analytics data
        analytics_query = text("""
            WITH activity_stats AS (
                SELECT 
                    a.activity_type,
                    COUNT(*) as count,
                    COUNT(CASE WHEN a.status = 'APPROVED' THEN 1 END) as approved_count,
                    COUNT(CASE WHEN a.status = 'REJECTED' THEN 1 END) as rejected_count,
                    COUNT(CASE WHEN a.status = 'PENDING' THEN 1 END) as pending_count,
                    COALESCE(SUM(a.credits), 0) as total_credits,
                    COALESCE(AVG(a.credits), 0) as avg_credits
                FROM activities a
                GROUP BY a.activity_type
            ),
            department_stats AS (
                SELECT 
                    u.department,
                    COUNT(DISTINCT CASE WHEN u.role = 'STUDENT' THEN u.id END) as students,
                    COUNT(DISTINCT CASE WHEN u.role = 'TEACHER' THEN u.id END) as teachers,
                    COUNT(DISTINCT a.id) as activities,
                    COALESCE(SUM(a.credits), 0) as total_credits
                FROM users u
                LEFT JOIN activities a ON u.id = a.user_id
                WHERE u.role IN ('STUDENT', 'TEACHER')
                GROUP BY u.department
            ),
            monthly_stats AS (
                SELECT 
                    strftime('%Y-%m', a.created_at) as month,
                    COUNT(*) as activities,
                    COUNT(CASE WHEN a.status = 'APPROVED' THEN 1 END) as approved,
                    COALESCE(SUM(a.credits), 0) as credits
                FROM activities a
                WHERE a.created_at >= date('now', '-12 months')
                GROUP BY strftime('%Y-%m', a.created_at)
                ORDER BY month
            )
            SELECT 
                'activity_types' as data_type,
                json_object(
                    'labels', json_group_array(activity_type),
                    'datasets', json_array(
                        json_object(
                            'label', 'Total Activities',
                            'data', json_group_array(count),
                            'backgroundColor', json_array('#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40')
                        ),
                        json_object(
                            'label', 'Approved Activities',
                            'data', json_group_array(approved_count),
                            'backgroundColor', json_array('#4CAF50', '#4CAF50', '#4CAF50', '#4CAF50', '#4CAF50', '#4CAF50')
                        )
                    )
                ) as chart_data
            FROM activity_stats
            
            UNION ALL
            
            SELECT 
                'departments' as data_type,
                json_object(
                    'labels', json_group_array(department),
                    'datasets', json_array(
                        json_object(
                            'label', 'Students',
                            'data', json_group_array(students),
                            'backgroundColor', '#36A2EB'
                        ),
                        json_object(
                            'label', 'Teachers',
                            'data', json_group_array(teachers),
                            'backgroundColor', '#FF6384'
                        ),
                        json_object(
                            'label', 'Activities',
                            'data', json_group_array(activities),
                            'backgroundColor', '#FFCE56'
                        )
                    )
                ) as chart_data
            FROM department_stats
            
            UNION ALL
            
            SELECT 
                'monthly_trends' as data_type,
                json_object(
                    'labels', json_group_array(month),
                    'datasets', json_array(
                        json_object(
                            'label', 'Total Activities',
                            'data', json_group_array(activities),
                            'borderColor', '#36A2EB',
                            'fill', false
                        ),
                        json_object(
                            'label', 'Approved Activities',
                            'data', json_group_array(approved),
                            'borderColor', '#4CAF50',
                            'fill', false
                        ),
                        json_object(
                            'label', 'Credits Awarded',
                            'data', json_group_array(credits),
                            'borderColor', '#FFCE56',
                            'fill', false
                        )
                    )
                ) as chart_data
            FROM monthly_stats
        """)
        
        result = db.execute(analytics_query).fetchall()
        
        # Convert to dictionary format
        analytics_data = {}
        for row in result:
            analytics_data[row.data_type] = json.loads(row.chart_data)
        
        return analytics_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics dashboard data: {str(e)}"
        )

