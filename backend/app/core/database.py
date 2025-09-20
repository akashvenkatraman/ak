from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import os

# Use Supabase PostgreSQL connection if available, otherwise fallback to local
if settings.database_url:
    SQLALCHEMY_DATABASE_URL = settings.database_url
else:
    # Construct from Supabase URL if available
    if settings.supabase_url != "your_supabase_url_here":
        # For Supabase, you need to provide the database password
        # Get this from your Supabase project settings > Database > Connection string
        # Format: postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
        if settings.database_password:
            # URL encode the password to handle special characters like @
            import urllib.parse
            encoded_password = urllib.parse.quote_plus(settings.database_password)
            # Use the correct Supabase hostname format
            SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{encoded_password}@db.ieugtoltckngbxreohcv.supabase.co:5432/postgres"
        else:
            # Fallback to local database if no password provided
            SQLALCHEMY_DATABASE_URL = "sqlite:///./certificate_management.db"
    else:
        # Local development database
        SQLALCHEMY_DATABASE_URL = "sqlite:///./certificate_management.db"

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={
            "connect_timeout": 10,
            "application_name": "certificate_management"
        }
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)
