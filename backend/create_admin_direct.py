#!/usr/bin/env python3
"""
Direct admin user creation script
This script creates the admin user directly using SQL
"""

import urllib.parse
from sqlalchemy import create_engine, text
from config import settings
import hashlib
import secrets

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    import bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_admin_directly():
    """Create admin user directly using SQL"""
    print("👤 Creating admin user directly...")
    
    try:
        # Create connection string
        encoded_password = urllib.parse.quote_plus(settings.database_password)
        db_url = f"postgresql://postgres:{encoded_password}@db.ieugtoltckngbxreohcv.supabase.co:5432/postgres"
        
        # Create engine
        engine = create_engine(db_url)
        
        with engine.begin() as conn:
            # Check if admin already exists
            result = conn.execute(text("SELECT id FROM users WHERE email = 'admin@example.com'"))
            if result.fetchone():
                print("ℹ️  Admin user already exists")
                return True
            
            # Hash the password
            hashed_password = hash_password("admin123456")
            
            # Insert admin user directly
            conn.execute(text("""
                INSERT INTO users (email, username, full_name, hashed_password, role, status, is_active, created_at)
                VALUES (:email, :username, :full_name, :hashed_password, :role, :status, :is_active, NOW())
            """), {
                'email': 'admin@example.com',
                'username': 'admin',
                'full_name': 'System Administrator',
                'hashed_password': hashed_password,
                'role': 'ADMIN',
                'status': 'APPROVED',
                'is_active': True
            })
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
    print("🚀 Creating admin user directly...")
    print("=" * 60)
    
    if create_admin_directly():
        print("\n" + "=" * 60)
        print("🎉 Admin user created successfully!")
        print("\n📋 Next steps:")
        print("1. Start the backend server: uvicorn main:app --reload")
        print("2. Start the frontend: cd ../frontend && npm start")
        print("3. Login as admin: admin@example.com / admin123456")
        print("4. Approve user registrations from the admin dashboard")
        return True
    else:
        print("\n❌ Failed to create admin user!")
        return False

if __name__ == "__main__":
    main()
