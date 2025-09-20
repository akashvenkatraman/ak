#!/usr/bin/env python3
"""
Migrate OAuth and Verification Fields
"""

import urllib.parse
from sqlalchemy import create_engine, text
from config import settings

def migrate_oauth_fields():
    """Add OAuth and verification fields to users table"""
    print("🔧 Migrating OAuth and verification fields to users table...")
    try:
        encoded_password = urllib.parse.quote_plus(settings.database_password)
        db_url = f"postgresql://postgres:{encoded_password}@db.ieugtoltckngbxreohcv.supabase.co:5432/postgres"
        engine = create_engine(db_url)

        with engine.connect() as conn:
            trans = conn.begin()
            try:
                print("📝 Adding OAuth and verification fields to users table...")
                
                # Add OAuth and verification columns if they don't exist
                conn.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN IF NOT EXISTS is_oauth_user BOOLEAN DEFAULT FALSE,
                    ADD COLUMN IF NOT EXISTS verification_code VARCHAR,
                    ADD COLUMN IF NOT EXISTS verification_expires TIMESTAMP;
                """))
                
                trans.commit()
                print("✅ OAuth and verification fields migration completed successfully!")
                return True
                
            except Exception as e:
                trans.rollback()
                print(f"❌ Error migrating OAuth fields: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Migrating OAuth and verification fields...")
    print("=" * 60)
    if migrate_oauth_fields():
        print("\n" + "=" * 60)
        print("🎉 OAuth and verification fields migration completed successfully!")
        print("\n📋 Fields added:")
        print("- is_oauth_user (BOOLEAN) - Whether user was created via OAuth")
        print("- verification_code (VARCHAR) - For password reset verification")
        print("- verification_expires (TIMESTAMP) - Verification code expiration")
    else:
        print("\n❌ OAuth and verification fields migration failed!")
