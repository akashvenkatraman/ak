-- RLS Policies for Storage Buckets
-- Run these commands in your Supabase SQL Editor

-- Enable RLS on storage.objects table
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Policy for user-images bucket
CREATE POLICY "Users can upload to user-images" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'user-images' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can view their user-images" ON storage.objects
FOR SELECT USING (
  bucket_id = 'user-images' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update their user-images" ON storage.objects
FOR UPDATE USING (
  bucket_id = 'user-images' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete their user-images" ON storage.objects
FOR DELETE USING (
  bucket_id = 'user-images' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy for profile-pictures bucket
CREATE POLICY "Users can upload to profile-pictures" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'profile-pictures' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can view their profile-pictures" ON storage.objects
FOR SELECT USING (
  bucket_id = 'profile-pictures' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update their profile-pictures" ON storage.objects
FOR UPDATE USING (
  bucket_id = 'profile-pictures' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete their profile-pictures" ON storage.objects
FOR DELETE USING (
  bucket_id = 'profile-pictures' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy for activity-documents bucket
CREATE POLICY "Users can upload to activity-documents" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'activity-documents' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can view their activity-documents" ON storage.objects
FOR SELECT USING (
  bucket_id = 'activity-documents' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update their activity-documents" ON storage.objects
FOR UPDATE USING (
  bucket_id = 'activity-documents' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete their activity-documents" ON storage.objects
FOR DELETE USING (
  bucket_id = 'activity-documents' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

