#!/usr/bin/env python3
"""
Setup Storage Policies for Supabase Storage Buckets
This script provides the correct SQL commands for storage policies
"""

def get_storage_policies():
    """Get the correct storage policies for Supabase"""
    
    policies = {
        "user-images": """
-- User Images Bucket Policies
-- Go to Storage → Policies → user-images → New Policy

-- Policy 1: Allow authenticated users to upload images
CREATE POLICY "Users can upload images" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'user-images' AND
  auth.role() = 'authenticated'
);

-- Policy 2: Allow users to view their own images
CREATE POLICY "Users can view own images" ON storage.objects
FOR SELECT USING (
  bucket_id = 'user-images' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy 3: Allow users to update their own images
CREATE POLICY "Users can update own images" ON storage.objects
FOR UPDATE USING (
  bucket_id = 'user-images' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy 4: Allow users to delete their own images
CREATE POLICY "Users can delete own images" ON storage.objects
FOR DELETE USING (
  bucket_id = 'user-images' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
""",

        "profile-pictures": """
-- Profile Pictures Bucket Policies
-- Go to Storage → Policies → profile-pictures → New Policy

-- Policy 1: Allow authenticated users to upload profile pictures
CREATE POLICY "Users can upload profile pictures" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'profile-pictures' AND
  auth.role() = 'authenticated'
);

-- Policy 2: Allow users to view their own profile pictures
CREATE POLICY "Users can view own profile pictures" ON storage.objects
FOR SELECT USING (
  bucket_id = 'profile-pictures' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy 3: Allow users to update their own profile pictures
CREATE POLICY "Users can update own profile pictures" ON storage.objects
FOR UPDATE USING (
  bucket_id = 'profile-pictures' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy 4: Allow users to delete their own profile pictures
CREATE POLICY "Users can delete own profile pictures" ON storage.objects
FOR DELETE USING (
  bucket_id = 'profile-pictures' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
""",

        "activity-documents": """
-- Activity Documents Bucket Policies
-- Go to Storage → Policies → activity-documents → New Policy

-- Policy 1: Allow authenticated users to upload activity documents
CREATE POLICY "Users can upload activity documents" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'activity-documents' AND
  auth.role() = 'authenticated'
);

-- Policy 2: Allow users to view their own activity documents
CREATE POLICY "Users can view own activity documents" ON storage.objects
FOR SELECT USING (
  bucket_id = 'activity-documents' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy 3: Allow teachers to view student documents
CREATE POLICY "Teachers can view student documents" ON storage.objects
FOR SELECT USING (
  bucket_id = 'activity-documents' AND
  EXISTS (
    SELECT 1 FROM teacher_student_associations tsa
    WHERE tsa.teacher_id = auth.uid()::int
    AND tsa.student_id = (storage.foldername(name))[1]::int
  )
);

-- Policy 4: Allow users to update their own activity documents
CREATE POLICY "Users can update own activity documents" ON storage.objects
FOR UPDATE USING (
  bucket_id = 'activity-documents' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy 5: Allow users to delete their own activity documents
CREATE POLICY "Users can delete own activity documents" ON storage.objects
FOR DELETE USING (
  bucket_id = 'activity-documents' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
"""
    }
    
    return policies

def print_manual_setup_guide():
    """Print manual setup guide"""
    print("🔧 Supabase Storage Policies Setup Guide")
    print("=" * 60)
    print()
    print("Since the storage.objects table requires special permissions,")
    print("we need to set up policies through the Supabase dashboard.")
    print()
    print("📋 Step-by-Step Instructions:")
    print()
    print("1. Go to your Supabase dashboard")
    print("2. Click 'Storage' in the left sidebar")
    print("3. Click 'Policies' tab (next to 'Buckets')")
    print("4. For each bucket, click 'New Policy' and add the policies below")
    print()
    
    policies = get_storage_policies()
    
    for bucket_name, policy_sql in policies.items():
        print(f"📦 {bucket_name.upper()} BUCKET POLICIES")
        print("-" * 40)
        print("Copy and paste these policies one by one:")
        print()
        print(policy_sql)
        print()
        print("=" * 60)
        print()

def print_alternative_approach():
    """Print alternative approach using bucket settings"""
    print("🔄 Alternative Approach: Use Bucket Settings")
    print("=" * 50)
    print()
    print("If the policies approach doesn't work, you can:")
    print()
    print("1. Go to Storage → Buckets")
    print("2. Click on each bucket (user-images, profile-pictures, activity-documents)")
    print("3. Go to 'Settings' tab")
    print("4. Set 'Public' to TRUE")
    print("5. This will make all files in the bucket publicly accessible")
    print()
    print("⚠️  Note: This is less secure but will work for testing")
    print("   You can add proper authentication later in your application code")

def main():
    """Main function"""
    print_manual_setup_guide()
    print_alternative_approach()
    
    print("\n🎯 Next Steps:")
    print("1. Follow the manual setup guide above")
    print("2. Or use the alternative approach for testing")
    print("3. Run: python test_storage_setup.py")
    print("4. Test file uploads through your API")

if __name__ == "__main__":
    main()
