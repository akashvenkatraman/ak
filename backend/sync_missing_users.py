#!/usr/bin/env python3
"""
Sync missing users to Supabase
"""

import requests
import json
from config import settings
from app.core.database import get_db
from sqlalchemy import text

def sync_missing_users():
    print("🔄 Syncing missing users to Supabase...")
    
    # Get local database
    db = next(get_db())
    
    # Get users that need to be synced
    users_to_sync = [
        {"id": 6, "email": "teststudent2@example.com", "name": "Test Student 2"},
        {"id": 7, "email": "akashvenkatraman10@gmail.com", "name": "Akash Venkatraman"},
        {"id": 8, "email": "teacher@gmail.com", "name": "teacher"}
    ]
    
    # Get user details from local database
    for user_info in users_to_sync:
        user_result = db.execute(text("""
            SELECT id, email, username, full_name, hashed_password, role, status, is_active, 
                   phone_number, department, student_id, employee_id, performance_score, 
                   total_credits_earned, created_at
            FROM users WHERE id = :id
        """), {"id": user_info["id"]}).fetchone()
        
        if user_result:
            print(f"\n📋 Syncing user: {user_result.full_name} ({user_result.email})")
            
            # Prepare data for Supabase
            supabase_user = {
                "id": user_result.id,
                "email": user_result.email,
                "username": user_result.username,
                "full_name": user_result.full_name,
                "hashed_password": user_result.hashed_password,
                "role": user_result.role.upper(),
                "status": user_result.status.upper(),
                "is_active": bool(user_result.is_active),
                "phone_number": user_result.phone_number,
                "department": user_result.department,
                "student_id": user_result.student_id,
                "employee_id": user_result.employee_id,
                "performance_score": user_result.performance_score or 0,
                "total_credits_earned": user_result.total_credits_earned or 0,
                "created_at": user_result.created_at if user_result.created_at else None
            }
            
            # Sync to Supabase
            url = f"{settings.supabase_url}/rest/v1/users"
            headers = {
                "apikey": settings.supabase_key,
                "Authorization": f"Bearer {settings.supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
            
            try:
                response = requests.post(url, headers=headers, json=[supabase_user])
                print(f"  📡 Response: {response.status_code} - {response.text}")
                
                if response.status_code in [200, 201]:
                    print(f"  ✅ Successfully synced {user_result.full_name}")
                else:
                    print(f"  ❌ Failed to sync {user_result.full_name}")
                    
            except Exception as e:
                print(f"  ❌ Error syncing {user_result.full_name}: {e}")

if __name__ == "__main__":
    sync_missing_users()
