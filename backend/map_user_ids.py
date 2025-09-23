#!/usr/bin/env python3
"""
Map user IDs between local and Supabase databases
"""

import requests
from config import settings
from app.core.database import get_db
from app.models.user import User, TeacherStudentAllocation

def map_user_ids():
    print("🔍 Mapping user IDs between local and Supabase...")
    
    # Get local database
    db = next(get_db())
    
    # Get local users using raw SQL
    from sqlalchemy import text
    local_users_result = db.execute(text("SELECT id, email, full_name, role, status FROM users")).fetchall()
    print("\n📊 LOCAL USERS:")
    for user in local_users_result:
        print(f"  ID: {user.id}, Email: {user.email}, Name: {user.full_name}, Role: {user.role}, Status: {user.status}")
    
    # Get Supabase users
    url = f"{settings.supabase_url}/rest/v1/users"
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            supabase_users = response.json()
            print("\n📊 SUPABASE USERS:")
            for user in supabase_users:
                print(f"  ID: {user['id']}, Email: {user['email']}, Name: {user['full_name']}, Role: {user['role']}")
            
            # Create mapping
            print("\n🔄 MAPPING:")
            email_to_supabase_id = {user['email']: user['id'] for user in supabase_users}
            
            for local_user in local_users_result:
                supabase_id = email_to_supabase_id.get(local_user.email)
                if supabase_id:
                    print(f"  Local ID {local_user.id} ({local_user.email}) -> Supabase ID {supabase_id}")
                else:
                    print(f"  ❌ Local ID {local_user.id} ({local_user.email}) -> NOT FOUND in Supabase")
            
            # Check allocations
            print("\n📋 ALLOCATIONS:")
            allocations_result = db.execute(text("SELECT teacher_id, student_id, allocated_by FROM teacher_student_allocations")).fetchall()
            for allocation in allocations_result:
                teacher_result = db.execute(text("SELECT email FROM users WHERE id = :id"), {"id": allocation.teacher_id}).fetchone()
                student_result = db.execute(text("SELECT email FROM users WHERE id = :id"), {"id": allocation.student_id}).fetchone()
                
                teacher_email = teacher_result.email if teacher_result else 'Unknown'
                student_email = student_result.email if student_result else 'Unknown'
                
                teacher_supabase_id = email_to_supabase_id.get(teacher_email)
                student_supabase_id = email_to_supabase_id.get(student_email)
                
                print(f"  Teacher: {teacher_email} (Local: {allocation.teacher_id}, Supabase: {teacher_supabase_id})")
                print(f"  Student: {student_email} (Local: {allocation.student_id}, Supabase: {student_supabase_id})")
                print(f"  Allocated by: {allocation.allocated_by}")
                print()
                
        else:
            print(f"❌ Failed to get Supabase users: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    map_user_ids()
