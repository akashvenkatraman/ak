from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import os
import urllib.parse

# Use local SQLite database with Supabase REST API for real-time synchronization
# This ensures reliable local data storage while maintaining Supabase sync capability
SQLALCHEMY_DATABASE_URL = "sqlite:///./certificate_management.db"
print("🔗 Using local SQLite database with Supabase REST API sync")

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
            "connect_timeout": 30,
            "application_name": "certificate_management",
            "options": "-c timezone=utc"
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
