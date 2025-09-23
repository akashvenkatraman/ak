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

router = APIRouter(prefix="/admin", tags=["Sample Data"])

# Sample college data
SAMPLE_TEACHERS_DATA = [
    {
        "id": 1,
        "name": "Dr. Sarah Johnson",
        "email": "sarah.johnson@college.edu",
        "department": "Computer Science",
        "employee_id": "CS001",
        "performance_score": 95,
        "total_credits_earned": 150,
        "assigned_students_count": 25,
        "total_activities_reviewed": 120,
        "approved_activities": 110,
        "rejected_activities": 5,
        "pending_activities": 5,
        "total_credits_awarded": 2200,
        "average_credits_per_activity": 18.3,
        "activities_last_30_days": 15,
        "activities_last_90_days": 45,
        "activities_last_year": 120,
        "approval_rate": 91.7,
        "rejection_rate": 4.2,
        "activity_review_efficiency": 4.8,
        "created_at": "2023-01-15",
        "last_updated": "2024-09-22"
    },
    {
        "id": 2,
        "name": "Prof. Michael Chen",
        "email": "michael.chen@college.edu",
        "department": "Mathematics",
        "employee_id": "MATH002",
        "performance_score": 88,
        "total_credits_earned": 135,
        "assigned_students_count": 30,
        "total_activities_reviewed": 95,
        "approved_activities": 85,
        "rejected_activities": 8,
        "pending_activities": 2,
        "total_credits_awarded": 1800,
        "average_credits_per_activity": 18.9,
        "activities_last_30_days": 12,
        "activities_last_90_days": 35,
        "activities_last_year": 95,
        "approval_rate": 89.5,
        "rejection_rate": 8.4,
        "activity_review_efficiency": 3.2,
        "created_at": "2023-02-20",
        "last_updated": "2024-09-22"
    },
    {
        "id": 3,
        "name": "Dr. Emily Rodriguez",
        "email": "emily.rodriguez@college.edu",
        "department": "Physics",
        "employee_id": "PHY003",
        "performance_score": 92,
        "total_credits_earned": 140,
        "assigned_students_count": 20,
        "total_activities_reviewed": 80,
        "approved_activities": 75,
        "rejected_activities": 3,
        "pending_activities": 2,
        "total_credits_awarded": 1600,
        "average_credits_per_activity": 20.0,
        "activities_last_30_days": 10,
        "activities_last_90_days": 28,
        "activities_last_year": 80,
        "approval_rate": 93.8,
        "rejection_rate": 3.8,
        "activity_review_efficiency": 4.0,
        "created_at": "2023-03-10",
        "last_updated": "2024-09-22"
    }
]

SAMPLE_STUDENTS_DATA = [
    {
        "id": 1,
        "name": "Alex Thompson",
        "email": "alex.thompson@student.college.edu",
        "department": "Computer Science",
        "student_id": "CS2024001",
        "performance_score": 87,
        "total_credits_earned": 45,
        "assigned_teacher": "Dr. Sarah Johnson",
        "total_activities": 12,
        "approved_activities": 10,
        "rejected_activities": 1,
        "pending_activities": 1,
        "total_credits_from_activities": 180,
        "average_credits_per_activity": 15.0,
        "activities_last_30_days": 3,
        "activities_last_90_days": 8,
        "activities_last_year": 12,
        "certificate_activities": 4,
        "project_activities": 3,
        "internship_activities": 2,
        "research_activities": 2,
        "seminar_activities": 1,
        "workshop_activities": 0,
        "success_rate": 83.3,
        "activity_completion_rate": 91.7,
        "credits_per_month": 7.5,
        "allocation_date": "2024-01-15",
        "created_at": "2024-01-10",
        "last_updated": "2024-09-22"
    },
    {
        "id": 2,
        "name": "Maria Garcia",
        "email": "maria.garcia@student.college.edu",
        "department": "Mathematics",
        "student_id": "MATH2024002",
        "performance_score": 94,
        "total_credits_earned": 52,
        "assigned_teacher": "Prof. Michael Chen",
        "total_activities": 15,
        "approved_activities": 14,
        "rejected_activities": 0,
        "pending_activities": 1,
        "total_credits_from_activities": 210,
        "average_credits_per_activity": 14.0,
        "activities_last_30_days": 4,
        "activities_last_90_days": 10,
        "activities_last_year": 15,
        "certificate_activities": 5,
        "project_activities": 4,
        "internship_activities": 3,
        "research_activities": 2,
        "seminar_activities": 1,
        "workshop_activities": 0,
        "success_rate": 93.3,
        "activity_completion_rate": 93.3,
        "credits_per_month": 8.7,
        "allocation_date": "2024-01-20",
        "created_at": "2024-01-15",
        "last_updated": "2024-09-22"
    },
    {
        "id": 3,
        "name": "James Wilson",
        "email": "james.wilson@student.college.edu",
        "department": "Physics",
        "student_id": "PHY2024003",
        "performance_score": 79,
        "total_credits_earned": 38,
        "assigned_teacher": "Dr. Emily Rodriguez",
        "total_activities": 10,
        "approved_activities": 8,
        "rejected_activities": 1,
        "pending_activities": 1,
        "total_credits_from_activities": 150,
        "average_credits_per_activity": 15.0,
        "activities_last_30_days": 2,
        "activities_last_90_days": 6,
        "activities_last_year": 10,
        "certificate_activities": 3,
        "project_activities": 2,
        "internship_activities": 2,
        "research_activities": 2,
        "seminar_activities": 1,
        "workshop_activities": 0,
        "success_rate": 80.0,
        "activity_completion_rate": 90.0,
        "credits_per_month": 6.3,
        "allocation_date": "2024-02-01",
        "created_at": "2024-01-25",
        "last_updated": "2024-09-22"
    }
]

SAMPLE_OVERALL_DATA = [
    {
        "department": "Computer Science",
        "total_students": 150,
        "total_teachers": 8,
        "total_activities": 450,
        "approved_activities": 420,
        "total_credits": 8500,
        "avg_credits_per_activity": 18.9,
        "research_activities": 120,
        "project_activities": 180,
        "internship_activities": 100,
        "total_departments": 1,
        "student_teacher_ratio": 18.8,
        "activity_approval_rate": 93.3,
        "activities_per_student": 3.0,
        "research_intensity": 26.7,
        "project_intensity": 40.0,
        "internship_intensity": 22.2,
        "overall_performance_score": 88.5
    },
    {
        "department": "Mathematics",
        "total_students": 120,
        "total_teachers": 6,
        "total_activities": 380,
        "approved_activities": 350,
        "total_credits": 7200,
        "avg_credits_per_activity": 18.9,
        "research_activities": 95,
        "project_activities": 150,
        "internship_activities": 80,
        "total_departments": 1,
        "student_teacher_ratio": 20.0,
        "activity_approval_rate": 92.1,
        "activities_per_student": 3.2,
        "research_intensity": 25.0,
        "project_intensity": 39.5,
        "internship_intensity": 21.1,
        "overall_performance_score": 87.2
    },
    {
        "department": "Physics",
        "total_students": 80,
        "total_teachers": 5,
        "total_activities": 250,
        "approved_activities": 230,
        "total_credits": 4800,
        "avg_credits_per_activity": 19.2,
        "research_activities": 80,
        "project_activities": 100,
        "internship_activities": 50,
        "total_departments": 1,
        "student_teacher_ratio": 16.0,
        "activity_approval_rate": 92.0,
        "activities_per_student": 3.1,
        "research_intensity": 32.0,
        "project_intensity": 40.0,
        "internship_intensity": 20.0,
        "overall_performance_score": 89.8
    }
]

@router.get("/export/teachers-sample")
def export_teachers_sample_data():
    """Export sample teachers performance data to CSV"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Teacher ID', 'Email', 'Full Name', 'Department', 'Employee ID',
            'Performance Score', 'Total Credits Earned', 'Assigned Students',
            'Total Activities Reviewed', 'Approved Activities', 'Rejected Activities', 'Pending Activities',
            'Total Credits Awarded', 'Average Credits per Activity',
            'Activities (Last 30 Days)', 'Activities (Last 90 Days)', 'Activities (Last Year)',
            'Approval Rate (%)', 'Rejection Rate (%)', 'Activity Review Efficiency',
            'Created At', 'Last Updated'
        ])
        
        # Write data
        for teacher in SAMPLE_TEACHERS_DATA:
            writer.writerow([
                teacher['id'],
                teacher['email'],
                teacher['name'],
                teacher['department'],
                teacher['employee_id'],
                teacher['performance_score'],
                teacher['total_credits_earned'],
                teacher['assigned_students_count'],
                teacher['total_activities_reviewed'],
                teacher['approved_activities'],
                teacher['rejected_activities'],
                teacher['pending_activities'],
                teacher['total_credits_awarded'],
                teacher['average_credits_per_activity'],
                teacher['activities_last_30_days'],
                teacher['activities_last_90_days'],
                teacher['activities_last_year'],
                teacher['approval_rate'],
                teacher['rejection_rate'],
                teacher['activity_review_efficiency'],
                teacher['created_at'],
                teacher['last_updated']
            ])
        
        output.seek(0)
        
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=teachers_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export teachers sample data: {str(e)}"
        )

@router.get("/export/students-sample")
def export_students_sample_data():
    """Export sample students performance data to CSV"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
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
        
        # Write data
        for student in SAMPLE_STUDENTS_DATA:
            writer.writerow([
                student['id'],
                student['email'],
                student['name'],
                student['department'],
                student['student_id'],
                student['performance_score'],
                student['total_credits_earned'],
                student['assigned_teacher'],
                student['total_activities'],
                student['approved_activities'],
                student['rejected_activities'],
                student['pending_activities'],
                student['total_credits_from_activities'],
                student['average_credits_per_activity'],
                student['activities_last_30_days'],
                student['activities_last_90_days'],
                student['activities_last_year'],
                student['certificate_activities'],
                student['project_activities'],
                student['internship_activities'],
                student['research_activities'],
                student['seminar_activities'],
                student['workshop_activities'],
                student['success_rate'],
                student['activity_completion_rate'],
                student['credits_per_month'],
                student['allocation_date'],
                student['created_at'],
                student['last_updated']
            ])
        
        output.seek(0)
        
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=students_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export students sample data: {str(e)}"
        )

@router.get("/export/overall-sample")
def export_overall_sample_data():
    """Export sample overall college metrics to CSV"""
    try:
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
        for dept in SAMPLE_OVERALL_DATA:
            writer.writerow([
                dept['department'],
                dept['total_students'],
                dept['total_teachers'],
                dept['total_activities'],
                dept['approved_activities'],
                dept['total_credits'],
                dept['avg_credits_per_activity'],
                dept['research_activities'],
                dept['project_activities'],
                dept['internship_activities'],
                dept['total_departments'],
                dept['student_teacher_ratio'],
                dept['activity_approval_rate'],
                dept['activities_per_student'],
                dept['research_intensity'],
                dept['project_intensity'],
                dept['internship_intensity'],
                dept['overall_performance_score']
            ])
        
        output.seek(0)
        
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=overall_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export overall sample data: {str(e)}"
        )

@router.get("/analytics/sample-dashboard-data")
def get_sample_analytics_dashboard_data():
    """Get sample data for analytics dashboard with charts and metrics"""
    try:
        # Activity types data
        activity_types_data = {
            "labels": ["Certificates", "Projects", "Internships", "Research", "Seminars", "Workshops"],
            "datasets": [
                {
                    "label": "Total Activities",
                    "data": [120, 180, 100, 95, 60, 45],
                    "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"]
                },
                {
                    "label": "Approved Activities",
                    "data": [110, 165, 90, 85, 55, 40],
                    "backgroundColor": ["#4CAF50", "#4CAF50", "#4CAF50", "#4CAF50", "#4CAF50", "#4CAF50"]
                }
            ]
        }
        
        # Department data
        departments_data = {
            "labels": ["Computer Science", "Mathematics", "Physics"],
            "datasets": [
                {
                    "label": "Students",
                    "data": [150, 120, 80],
                    "backgroundColor": "#36A2EB"
                },
                {
                    "label": "Teachers",
                    "data": [8, 6, 5],
                    "backgroundColor": "#FF6384"
                },
                {
                    "label": "Activities",
                    "data": [450, 380, 250],
                    "backgroundColor": "#FFCE56"
                }
            ]
        }
        
        # Monthly trends data
        monthly_trends_data = {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
            "datasets": [
                {
                    "label": "Total Activities",
                    "data": [45, 52, 48, 61, 55, 58, 42, 38, 65],
                    "borderColor": "#36A2EB",
                    "fill": False
                },
                {
                    "label": "Approved Activities",
                    "data": [42, 48, 45, 57, 51, 54, 39, 35, 60],
                    "borderColor": "#4CAF50",
                    "fill": False
                },
                {
                    "label": "Credits Awarded",
                    "data": [850, 980, 920, 1150, 1040, 1100, 800, 720, 1230],
                    "borderColor": "#FFCE56",
                    "fill": False
                }
            ]
        }
        
        return {
            "activity_types": activity_types_data,
            "departments": departments_data,
            "monthly_trends": monthly_trends_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sample analytics dashboard data: {str(e)}"
        )

