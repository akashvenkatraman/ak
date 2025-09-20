#!/usr/bin/env python3
"""
Fix database constraints to accept lowercase enum values
"""

from app.core.database import engine
from sqlalchemy import text

def fix_constraints():
    """Fix database constraints"""
    print("🔧 Fixing database constraints...")
    
    try:
        with engine.begin() as conn:
            # Drop existing constraints
            print("📝 Dropping existing constraints...")
            conn.execute(text("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check"))
            conn.execute(text("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_status_check"))
            
            # Add new constraints with lowercase values
            print("📝 Adding new constraints...")
            conn.execute(text("""
                ALTER TABLE users ADD CONSTRAINT users_role_check 
                CHECK (role IN ('admin', 'teacher', 'student'))
            """))
            
            conn.execute(text("""
                ALTER TABLE users ADD CONSTRAINT users_status_check 
                CHECK (status IN ('pending', 'approved', 'rejected'))
            """))
            
            print("✅ Constraints updated successfully!")
            
            # Verify the data
            result = conn.execute(text("SELECT username, role, status FROM users"))
            users = result.fetchall()
            print(f"📊 Current users: {users}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error fixing constraints: {e}")
        return False

if __name__ == "__main__":
    fix_constraints()
