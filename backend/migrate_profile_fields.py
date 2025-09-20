#!/usr/bin/env python3
"""
Profile fields migration script for Supabase
This script adds comprehensive profile fields to the existing users table
"""

import urllib.parse
from sqlalchemy import create_engine, text
from config import settings

def migrate_profile_fields():
    """Add profile fields to existing users table"""
    print("🔧 Migrating profile fields to users table...")
    
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
                # Add profile fields to users table
                print("📝 Adding profile fields to users table...")
                
                # Add performance and credits fields
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS performance_score INTEGER DEFAULT 0;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS total_credits_earned INTEGER DEFAULT 0;
                """))
                
                # Add profile management fields
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS profile_picture VARCHAR;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS bio TEXT;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS date_of_birth TIMESTAMP;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS address TEXT;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS city VARCHAR;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS state VARCHAR;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS country VARCHAR;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS postal_code VARCHAR;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS linkedin_url VARCHAR;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS twitter_url VARCHAR;
                """))
                
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS website_url VARCHAR;
                """))
                
                # Add updated_at trigger
                print("📝 Adding updated_at trigger...")
                conn.execute(text("""
                    CREATE OR REPLACE FUNCTION update_updated_at_column()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.updated_at = NOW();
                        RETURN NEW;
                    END;
                    $$ language 'plpgsql';
                """))
                
                conn.execute(text("""
                    DROP TRIGGER IF EXISTS update_users_updated_at ON users;
                    CREATE TRIGGER update_users_updated_at
                        BEFORE UPDATE ON users
                        FOR EACH ROW
                        EXECUTE FUNCTION update_updated_at_column();
                """))
                
                # Commit transaction
                trans.commit()
                print("✅ Profile fields migration completed successfully!")
                return True
                
            except Exception as e:
                trans.rollback()
                print(f"❌ Error migrating profile fields: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Migrating profile fields to users table...")
    print("=" * 60)
    
    # Migrate profile fields
    if not migrate_profile_fields():
        print("\n❌ Failed to migrate profile fields!")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Profile fields migration completed successfully!")
    print("\n📋 Profile fields added:")
    print("- performance_score (INTEGER)")
    print("- total_credits_earned (INTEGER)")
    print("- profile_picture (VARCHAR)")
    print("- bio (TEXT)")
    print("- date_of_birth (TIMESTAMP)")
    print("- address (TEXT)")
    print("- city (VARCHAR)")
    print("- state (VARCHAR)")
    print("- country (VARCHAR)")
    print("- postal_code (VARCHAR)")
    print("- linkedin_url (VARCHAR)")
    print("- twitter_url (VARCHAR)")
    print("- website_url (VARCHAR)")
    print("- updated_at trigger for automatic timestamp updates")
    
    return True

if __name__ == "__main__":
    main()
