from supabase import create_client, Client
from config import settings

# Initialize Supabase client
supabase: Client = create_client(
    settings.supabase_url,
    settings.supabase_key
)

def get_supabase_client() -> Client:
    """Get the Supabase client instance"""
    return supabase





