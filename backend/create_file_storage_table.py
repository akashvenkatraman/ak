#!/usr/bin/env python3
"""Create file storage table for managing uploaded files"""

from app.core.database import SessionLocal, engine
from sqlalchemy import text

def create_file_storage_table():
    """Create file_storage table for managing uploaded files"""
    try:
        db = SessionLocal()
        
        # Create file_storage table
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS file_storage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                supabase_url TEXT,
                file_size INTEGER NOT NULL,
                content_type TEXT NOT NULL,
                file_type TEXT NOT NULL CHECK (file_type IN ('certificate', 'profile_picture', 'document')),
                user_id INTEGER NOT NULL,
                activity_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (activity_id) REFERENCES activities (id) ON DELETE SET NULL
            )
        """))
        
        # Create indexes for better performance (after table creation)
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_file_storage_user_id ON file_storage (user_id)"))
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_file_storage_file_type ON file_storage (file_type)"))
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_file_storage_activity_id ON file_storage (activity_id)"))
        
        db.commit()
        db.close()
        
        print("✅ File storage table created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating file storage table: {e}")
        return False

if __name__ == "__main__":
    create_file_storage_table()
