from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Supabase Configuration
    supabase_url: str = "https://ieugtoltckngbxreohcv.supabase.co"
    supabase_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlldWd0b2x0Y2tuZ2J4cmVvaGN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyOTgwNjEsImV4cCI6MjA3Mzg3NDA2MX0.UIR-69xAM1vUJDc7Y9KC4fYrCBHTS-56M4qtzRqMShk"
    supabase_service_key: str = "your_supabase_service_key_here"  # You'll need to get this from Supabase dashboard
    
    # JWT Configuration
    secret_key: str = "Dkq5f+z+8bsnHu+Dqa2fZSncaCGvC1dgYzFITE773w6H1IX94GiPk7WYQNlYGcTEz9Cz00JEz+RwlEig7/umGA=="
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database Configuration
    database_url: Optional[str] = None
    database_password: Optional[str] = "AKASHvenkat@10"  # Supabase database password
    
    # Application Configuration
    debug: bool = True
    host: str = "localhost"
    port: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
