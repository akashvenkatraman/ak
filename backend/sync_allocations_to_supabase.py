#!/usr/bin/env python3
"""
Script to sync existing teacher-student allocations to Supabase
"""

from app.core.database import get_db
from app.core.supabase_client import get_supabase_client
from app.models.user import TeacherStudentAllocation

def sync_allocations_to_supabase():
    print("🔄 Syncing teacher-student allocations to Supabase...")
    
    # Get database connection
    db = next(get_db())
    
    # Get all allocations
    allocations = db.query(TeacherStudentAllocation).all()
    print(f"📊 Found {len(allocations)} allocations in local database")
    
    if not allocations:
        print("ℹ️ No allocations to sync")
        return
    
    try:
        # Get Supabase client
        supabase = get_supabase_client()
        
        # Prepare data for Supabase
        supabase_data = []
        for allocation in allocations:
            supabase_data.append({
                "id": allocation.id,
                "teacher_id": allocation.teacher_id,
                "student_id": allocation.student_id,
                "allocated_by": allocation.allocated_by,
                "created_at": allocation.created_at.isoformat() if allocation.created_at else None
            })
        
        # Insert into Supabase
        result = supabase.table("teacher_student_allocations").upsert(supabase_data).execute()
        print(f"✅ Successfully synced {len(supabase_data)} allocations to Supabase")
        print(f"📋 Supabase response: {result}")
        
    except Exception as e:
        print(f"❌ Failed to sync allocations to Supabase: {e}")
        print(f"🔍 Error details: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    sync_allocations_to_supabase()
