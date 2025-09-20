#!/usr/bin/env python3
"""
Database migration script to add new tables for activity logging and file storage
"""

import urllib.parse
from sqlalchemy import create_engine, text
from config import settings

def migrate_database():
    """Add new tables for activity logging and file storage"""
    print("🔄 Starting database migration...")
    
    try:
        # Create connection string
        encoded_password = urllib.parse.quote_plus(settings.database_password)
        db_url = f"postgresql://postgres:{encoded_password}@db.ieugtoltckngbxreohcv.supabase.co:5432/postgres"
        
        # Create engine
        engine = create_engine(db_url)
        
        with engine.begin() as conn:
            print("📋 Creating activity_logs table...")
            
            # Create activity_logs table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id SERIAL PRIMARY KEY,
                    activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    log_type VARCHAR(50) NOT NULL,
                    description TEXT NOT NULL,
                    log_metadata JSONB,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """))
            
            print("📋 Creating file_storage table...")
            
            # Create file_storage table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS file_storage (
                    id SERIAL PRIMARY KEY,
                    activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
                    file_name VARCHAR(255) NOT NULL,
                    original_name VARCHAR(255) NOT NULL,
                    file_path VARCHAR(500) NOT NULL,
                    file_size INTEGER NOT NULL,
                    file_type VARCHAR(100) NOT NULL,
                    file_extension VARCHAR(10) NOT NULL,
                    uploaded_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    is_certificate BOOLEAN DEFAULT TRUE,
                    download_count INTEGER DEFAULT 0,
                    view_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """))
            
            print("📋 Adding files_count column to activities table...")
            
            # Add files_count column to activities table
            try:
                conn.execute(text("""
                    ALTER TABLE activities 
                    ADD COLUMN IF NOT EXISTS files_count INTEGER DEFAULT 0
                """))
            except Exception as e:
                print(f"ℹ️  files_count column might already exist: {e}")
            
            print("📋 Creating indexes...")
            
            # Create indexes for better performance
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_activity_logs_activity_id 
                ON activity_logs(activity_id)
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_activity_logs_user_id 
                ON activity_logs(user_id)
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_activity_logs_log_type 
                ON activity_logs(log_type)
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_activity_logs_created_at 
                ON activity_logs(created_at)
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_file_storage_activity_id 
                ON file_storage(activity_id)
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_file_storage_uploaded_by 
                ON file_storage(uploaded_by)
            """))
            
            print("📋 Creating enum types...")
            
            # Create enum types for activity logs
            try:
                conn.execute(text("""
                    CREATE TYPE activity_log_type AS ENUM (
                        'activity_created',
                        'activity_updated', 
                        'activity_deleted',
                        'activity_submitted',
                        'activity_approved',
                        'activity_rejected',
                        'activity_under_review',
                        'certificate_uploaded',
                        'certificate_viewed',
                        'certificate_downloaded',
                        'comment_added',
                        'credits_awarded',
                        'status_changed'
                    )
                """)
                )
            except Exception as e:
                print(f"ℹ️  Activity log type enum might already exist: {e}")
            
            print("✅ Database migration completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    migrate_database()
