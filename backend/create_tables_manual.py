#!/usr/bin/env python3
"""
Manual table creation script for Supabase
This script creates all required tables in your Supabase database
"""

import urllib.parse
from sqlalchemy import create_engine, text
from config import settings

def create_tables_manually():
    """Create tables manually in Supabase"""
    print("🔧 Creating tables in Supabase...")
    
    try:
        # Create connection string
        encoded_password = urllib.parse.quote_plus(settings.database_password)
        db_url = f"postgresql://postgres:{encoded_password}@db.ieugtoltckngbxreohcv.supabase.co:5432/postgres"
        
        # Create engine
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                # Create users table
                print("📝 Creating users table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR UNIQUE NOT NULL,
                        username VARCHAR UNIQUE NOT NULL,
                        full_name VARCHAR NOT NULL,
                        hashed_password VARCHAR NOT NULL,
                        role VARCHAR NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
                        status VARCHAR DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
                        is_active BOOLEAN DEFAULT TRUE,
                        phone_number VARCHAR,
                        department VARCHAR,
                        student_id VARCHAR,
                        employee_id VARCHAR,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE
                    );
                """))
                
                # Create teacher_student_allocations table
                print("📝 Creating teacher_student_allocations table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS teacher_student_allocations (
                        id SERIAL PRIMARY KEY,
                        teacher_id INTEGER NOT NULL REFERENCES users(id),
                        student_id INTEGER NOT NULL REFERENCES users(id),
                        allocated_by INTEGER NOT NULL REFERENCES users(id),
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                """))
                
                # Create activities table
                print("📝 Creating activities table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS activities (
                        id SERIAL PRIMARY KEY,
                        student_id INTEGER NOT NULL REFERENCES users(id),
                        title VARCHAR NOT NULL,
                        description TEXT,
                        activity_type VARCHAR NOT NULL CHECK (activity_type IN ('seminar', 'conference', 'online_course', 'mooc', 'internship', 'extracurricular', 'workshop', 'certification')),
                        credits FLOAT DEFAULT 0.0,
                        start_date TIMESTAMP,
                        end_date TIMESTAMP,
                        certificate_file_path VARCHAR,
                        additional_documents TEXT,
                        status VARCHAR DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'under_review')),
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE
                    );
                """))
                
                # Create activity_approvals table
                print("📝 Creating activity_approvals table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS activity_approvals (
                        id SERIAL PRIMARY KEY,
                        activity_id INTEGER NOT NULL REFERENCES activities(id),
                        teacher_id INTEGER NOT NULL REFERENCES users(id),
                        status VARCHAR NOT NULL CHECK (status IN ('pending', 'approved', 'rejected', 'under_review')),
                        comments TEXT,
                        credits_awarded FLOAT DEFAULT 0.0,
                        approved_at TIMESTAMP WITH TIME ZONE,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                """))
                
                # Create student_performance table
                print("📝 Creating student_performance table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS student_performance (
                        id SERIAL PRIMARY KEY,
                        student_id INTEGER NOT NULL REFERENCES users(id),
                        semester VARCHAR NOT NULL,
                        academic_year VARCHAR NOT NULL,
                        gpa FLOAT,
                        attendance_percentage FLOAT,
                        total_credits FLOAT DEFAULT 0.0,
                        extracurricular_credits FLOAT DEFAULT 0.0,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE
                    );
                """))
                
                # Create indexes for better performance
                print("📝 Creating indexes...")
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_activities_student_id ON activities(student_id);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_activities_status ON activities(status);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_teacher_student_teacher_id ON teacher_student_allocations(teacher_id);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_teacher_student_student_id ON teacher_student_allocations(student_id);"))
                
                # Commit transaction
                trans.commit()
                print("✅ All tables created successfully!")
                return True
                
            except Exception as e:
                trans.rollback()
                print(f"❌ Error creating tables: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_admin_user():
    """Create admin user"""
    print("👤 Creating admin user...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.user import User, UserRole, UserStatus
        from app.core.auth import get_password_hash
        
        db = SessionLocal()
        
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
        if existing_admin:
            print("ℹ️  Admin user already exists")
            db.close()
            return True
        
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("admin123456"),
            full_name="System Administrator",
            role="admin",  # Use string instead of enum
            status="approved",  # Use string instead of enum
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.close()
        
        print("✅ Admin user created successfully!")
        print("   Email: admin@example.com")
        print("   Username: admin")
        print("   Password: admin123456")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Setting up Supabase tables manually...")
    print("=" * 60)
    
    # Create tables
    if not create_tables_manually():
        print("\n❌ Failed to create tables!")
        return False
    
    # Create admin user
    if not create_admin_user():
        print("\n❌ Failed to create admin user!")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the backend server: uvicorn main:app --reload")
    print("2. Start the frontend: cd ../frontend && npm start")
    print("3. Login as admin: admin@example.com / admin123456")
    print("4. Approve user registrations from the admin dashboard")
    
    return True

if __name__ == "__main__":
    main()
