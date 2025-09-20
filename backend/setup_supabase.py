#!/usr/bin/env python3
"""
Supabase Setup Script for Certificate Management Portal
This script helps you configure Supabase database connection
"""

import os
import sys
from sqlalchemy import create_engine, text
from config import settings

def test_database_connection():
    """Test the database connection"""
    print("🔍 Testing database connection...")
    
    # Try to connect to Supabase first
    if settings.database_password:
        try:
            import urllib.parse
            encoded_password = urllib.parse.quote_plus(settings.database_password)
            db_url = f"postgresql://postgres:{encoded_password}@db.ieugtoltckngbxreohcv.supabase.co:5432/postgres"
            print(f"🔍 Connection string: {db_url}")
            engine = create_engine(db_url)
            
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Successfully connected to Supabase PostgreSQL!")
                return True
        except Exception as e:
            print(f"❌ Failed to connect to Supabase: {e}")
            return False
    else:
        print("⚠️  No database password provided. Using local SQLite database.")
        return True

def create_tables():
    """Create database tables"""
    print("🔧 Creating database tables...")
    
    try:
        from app.core.database import create_tables
        create_tables()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
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
            role=UserRole.ADMIN,
            status=UserStatus.APPROVED,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.close()
        
        print("✅ Admin user created successfully!")
        print("   Email: admin@example.com")
        print("   Password: admin123456")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Certificate Management Portal with Supabase...")
    print("=" * 60)
    
    # Test database connection
    if not test_database_connection():
        print("\n❌ Database connection failed!")
        print("Please check your Supabase credentials and try again.")
        return False
    
    # Create tables
    if not create_tables():
        print("\n❌ Failed to create database tables!")
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
