#!/usr/bin/env python3
"""
Simple script to sync allocations using requests
"""

import requests
import json
from app.core.database import get_db
from app.models.user import TeacherStudentAllocation
from config import settings
from sqlalchemy import text

def sync_allocations_simple():
    print("🔄 Syncing teacher-student allocations to Supabase...")
    
    # Get database connection
    db = next(get_db())
    
    # Get all allocations
    allocations = db.query(TeacherStudentAllocation).all()
    print(f"📊 Found {len(allocations)} allocations in local database")
    
    if not allocations:
        print("ℹ️ No allocations to sync")
        return
    
    # Get Supabase user IDs
    url_users = f"{settings.supabase_url}/rest/v1/users"
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url_users, headers=headers)
    if response.status_code == 200:
        supabase_users = response.json()
        email_to_supabase_id = {user['email']: user['id'] for user in supabase_users}
        print(f"📋 Supabase user mapping: {email_to_supabase_id}")
    else:
        print(f"❌ Failed to get Supabase users: {response.text}")
        return
    
    # Prepare data for Supabase
    supabase_data = []
    for allocation in allocations:
        # Get teacher and student emails
        teacher_result = db.execute(text("SELECT email FROM users WHERE id = :id"), {"id": allocation.teacher_id}).fetchone()
        student_result = db.execute(text("SELECT email FROM users WHERE id = :id"), {"id": allocation.student_id}).fetchone()
        
        teacher_email = teacher_result.email if teacher_result else None
        student_email = student_result.email if student_result else None
        
        teacher_supabase_id = email_to_supabase_id.get(teacher_email)
        student_supabase_id = email_to_supabase_id.get(student_email)
        
        if teacher_supabase_id and student_supabase_id:
            supabase_data.append({
                "id": allocation.id,
                "teacher_id": teacher_supabase_id,
                "student_id": student_supabase_id,
                "allocated_by": 3,  # Use admin user ID from Supabase
                "created_at": allocation.created_at.isoformat() if allocation.created_at else None
            })
            print(f"✅ Mapped allocation: Teacher {teacher_email} (Supabase ID: {teacher_supabase_id}) -> Student {student_email} (Supabase ID: {student_supabase_id})")
        else:
            print(f"❌ Could not map allocation: Teacher {teacher_email} (Supabase ID: {teacher_supabase_id}) -> Student {student_email} (Supabase ID: {student_supabase_id})")
    
    print(f"📋 Data to sync: {json.dumps(supabase_data, indent=2)}")
    
    # Use Supabase REST API directly
    url = f"{settings.supabase_url}/rest/v1/teacher_student_allocations"
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }
    
    try:
        response = requests.post(url, headers=headers, json=supabase_data)
        print(f"📡 Supabase response status: {response.status_code}")
        print(f"📡 Supabase response: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ Successfully synced allocations to Supabase")
        else:
            print(f"❌ Failed to sync: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    sync_allocations_simple()
