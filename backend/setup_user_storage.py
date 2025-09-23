#!/usr/bin/env python3
"""
Supabase User Storage Setup Script
Creates storage buckets and RLS policies for user-specific image storage
"""

import requests
import json
from typing import Dict, List, Optional, Any
from config import settings

class SupabaseStorageSetup:
    def __init__(self):
        self.url = settings.supabase_url
        self.key = settings.supabase_key
        self.service_key = settings.supabase_service_key
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        self.service_headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def create_storage_bucket(self, bucket_name: str, public: bool = True, file_size_limit: int = 10, allowed_mime_types: List[str] = None) -> bool:
        """Create a storage bucket in Supabase"""
        try:
            bucket_data = {
                "id": bucket_name,
                "name": bucket_name,
                "public": public,
                "file_size_limit": file_size_limit * 1024 * 1024,  # Convert MB to bytes
                "allowed_mime_types": allowed_mime_types or []
            }
            
            response = requests.post(
                f"{self.url}/storage/v1/bucket",
                headers=self.service_headers,
                json=bucket_data,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Created bucket: {bucket_name}")
                return True
            elif response.status_code == 409:
                print(f"⚠️  Bucket already exists: {bucket_name}")
                return True
            else:
                print(f"❌ Failed to create bucket {bucket_name}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error creating bucket {bucket_name}: {e}")
            return False
    
    def create_rls_policy(self, policy_name: str, policy_sql: str) -> bool:
        """Create RLS policy for storage"""
        try:
            # Note: RLS policies need to be created via SQL
            # This is a placeholder - actual implementation would use Supabase SQL editor
            print(f"📝 Policy to create: {policy_name}")
            print(f"SQL: {policy_sql}")
            return True
        except Exception as e:
            print(f"❌ Error creating policy {policy_name}: {e}")
            return False
    
    def setup_user_images_bucket(self) -> bool:
        """Setup bucket for user-uploaded images"""
        print("🖼️  Setting up user images bucket...")
        
        # Create bucket
        success = self.create_storage_bucket(
            bucket_name="user-images",
            public=True,
            file_size_limit=10,  # 10MB
            allowed_mime_types=[
                "image/jpeg",
                "image/jpg", 
                "image/png",
                "image/gif",
                "image/webp"
            ]
        )
        
        if success:
            # Define RLS policies
            policies = [
                {
                    "name": "Users can upload images",
                    "sql": """
                    CREATE POLICY "Users can upload images" ON storage.objects
                    FOR INSERT WITH CHECK (
                        bucket_id = 'user-images' AND
                        auth.role() = 'authenticated'
                    );
                    """
                },
                {
                    "name": "Users can view their own images",
                    "sql": """
                    CREATE POLICY "Users can view own images" ON storage.objects
                    FOR SELECT USING (
                        bucket_id = 'user-images' AND
                        auth.uid()::text = (storage.foldername(name))[1]
                    );
                    """
                },
                {
                    "name": "Users can update their own images",
                    "sql": """
                    CREATE POLICY "Users can update own images" ON storage.objects
                    FOR UPDATE USING (
                        bucket_id = 'user-images' AND
                        auth.uid()::text = (storage.foldername(name))[1]
                    );
                    """
                },
                {
                    "name": "Users can delete their own images",
                    "sql": """
                    CREATE POLICY "Users can delete own images" ON storage.objects
                    FOR DELETE USING (
                        bucket_id = 'user-images' AND
                        auth.uid()::text = (storage.foldername(name))[1]
                    );
                    """
                }
            ]
            
            for policy in policies:
                self.create_rls_policy(policy["name"], policy["sql"])
        
        return success
    
    def setup_profile_pictures_bucket(self) -> bool:
        """Setup bucket for profile pictures"""
        print("👤 Setting up profile pictures bucket...")
        
        success = self.create_storage_bucket(
            bucket_name="profile-pictures",
            public=True,
            file_size_limit=5,  # 5MB
            allowed_mime_types=[
                "image/jpeg",
                "image/jpg",
                "image/png",
                "image/gif"
            ]
        )
        
        if success:
            policies = [
                {
                    "name": "Users can upload profile pictures",
                    "sql": """
                    CREATE POLICY "Users can upload profile pictures" ON storage.objects
                    FOR INSERT WITH CHECK (
                        bucket_id = 'profile-pictures' AND
                        auth.role() = 'authenticated'
                    );
                    """
                },
                {
                    "name": "Users can view their own profile pictures",
                    "sql": """
                    CREATE POLICY "Users can view own profile pictures" ON storage.objects
                    FOR SELECT USING (
                        bucket_id = 'profile-pictures' AND
                        auth.uid()::text = (storage.foldername(name))[1]
                    );
                    """
                },
                {
                    "name": "Users can update their own profile pictures",
                    "sql": """
                    CREATE POLICY "Users can update own profile pictures" ON storage.objects
                    FOR UPDATE USING (
                        bucket_id = 'profile-pictures' AND
                        auth.uid()::text = (storage.foldername(name))[1]
                    );
                    """
                },
                {
                    "name": "Users can delete their own profile pictures",
                    "sql": """
                    CREATE POLICY "Users can delete own profile pictures" ON storage.objects
                    FOR DELETE USING (
                        bucket_id = 'profile-pictures' AND
                        auth.uid()::text = (storage.foldername(name))[1]
                    );
                    """
                }
            ]
            
            for policy in policies:
                self.create_rls_policy(policy["name"], policy["sql"])
        
        return success
    
    def setup_activity_documents_bucket(self) -> bool:
        """Setup bucket for activity-related documents"""
        print("📄 Setting up activity documents bucket...")
        
        success = self.create_storage_bucket(
            bucket_name="activity-documents",
            public=True,
            file_size_limit=15,  # 15MB
            allowed_mime_types=[
                "application/pdf",
                "image/jpeg",
                "image/jpg",
                "image/png",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ]
        )
        
        if success:
            policies = [
                {
                    "name": "Users can upload activity documents",
                    "sql": """
                    CREATE POLICY "Users can upload activity documents" ON storage.objects
                    FOR INSERT WITH CHECK (
                        bucket_id = 'activity-documents' AND
                        auth.role() = 'authenticated'
                    );
                    """
                },
                {
                    "name": "Users can view their own activity documents",
                    "sql": """
                    CREATE POLICY "Users can view own activity documents" ON storage.objects
                    FOR SELECT USING (
                        bucket_id = 'activity-documents' AND
                        auth.uid()::text = (storage.foldername(name))[1]
                    );
                    """
                },
                {
                    "name": "Teachers can view student documents",
                    "sql": """
                    CREATE POLICY "Teachers can view student documents" ON storage.objects
                    FOR SELECT USING (
                        bucket_id = 'activity-documents' AND
                        EXISTS (
                            SELECT 1 FROM teacher_student_associations tsa
                            WHERE tsa.teacher_id = auth.uid()::int
                            AND tsa.student_id = (storage.foldername(name))[1]::int
                        )
                    );
                    """
                },
                {
                    "name": "Users can update their own activity documents",
                    "sql": """
                    CREATE POLICY "Users can update own activity documents" ON storage.objects
                    FOR UPDATE USING (
                        bucket_id = 'activity-documents' AND
                        auth.uid()::text = (storage.foldername(name))[1]
                    );
                    """
                },
                {
                    "name": "Users can delete their own activity documents",
                    "sql": """
                    CREATE POLICY "Users can delete own activity documents" ON storage.objects
                    FOR DELETE USING (
                        bucket_id = 'activity-documents' AND
                        auth.uid()::text = (storage.foldername(name))[1]
                    );
                    """
                }
            ]
            
            for policy in policies:
                self.create_rls_policy(policy["name"], policy["sql"])
        
        return success
    
    def test_storage_connection(self) -> bool:
        """Test connection to Supabase storage"""
        try:
            response = requests.get(
                f"{self.url}/storage/v1/bucket",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Supabase storage connection successful")
                return True
            else:
                print(f"❌ Supabase storage connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Supabase storage connection error: {e}")
            return False
    
    def list_existing_buckets(self) -> List[Dict[str, Any]]:
        """List existing storage buckets"""
        try:
            response = requests.get(
                f"{self.url}/storage/v1/bucket",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                buckets = response.json()
                print(f"📦 Found {len(buckets)} existing buckets:")
                for bucket in buckets:
                    print(f"   - {bucket.get('id', 'unknown')} (public: {bucket.get('public', False)})")
                return buckets
            else:
                print(f"❌ Failed to list buckets: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error listing buckets: {e}")
            return []
    
    def setup_all_storage(self) -> bool:
        """Setup all storage buckets and policies"""
        print("🚀 Starting Supabase Storage Setup...")
        print("=" * 50)
        
        # Test connection first
        if not self.test_storage_connection():
            print("❌ Cannot proceed without storage connection")
            return False
        
        # List existing buckets
        self.list_existing_buckets()
        print()
        
        # Setup buckets
        success = True
        success &= self.setup_user_images_bucket()
        print()
        success &= self.setup_profile_pictures_bucket()
        print()
        success &= self.setup_activity_documents_bucket()
        print()
        
        if success:
            print("✅ All storage buckets setup completed!")
            print("\n📋 Next Steps:")
            print("1. Go to your Supabase dashboard")
            print("2. Navigate to Storage section")
            print("3. Verify the buckets were created")
            print("4. Run the RLS policies in the SQL editor")
            print("5. Test file uploads through your application")
        else:
            print("❌ Some storage setup failed. Check the errors above.")
        
        return success

def main():
    """Main function to run the storage setup"""
    print("🎯 Supabase User Storage Setup")
    print("=" * 50)
    
    # Check if service key is configured
    if settings.supabase_service_key == "your_supabase_service_key_here":
        print("❌ Service key not configured!")
        print("Please update your config.py with the actual Supabase service key.")
        print("You can find it in your Supabase dashboard under Settings > API")
        return False
    
    # Initialize setup
    setup = SupabaseStorageSetup()
    
    # Run setup
    return setup.setup_all_storage()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Storage setup completed successfully!")
    else:
        print("\n💥 Storage setup failed. Please check the configuration.")
