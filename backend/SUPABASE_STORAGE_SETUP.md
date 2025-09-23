# Supabase Storage Setup Guide

## Overview
This guide will help you set up Supabase storage buckets for certificate and document uploads in the Smart Student Hub application.

## Prerequisites
- Supabase project created
- Supabase URL and API key configured
- Backend server running

## Manual Storage Bucket Setup

Since Supabase has Row Level Security (RLS) policies that prevent automatic bucket creation via API, you need to create the storage buckets manually in the Supabase dashboard.

### Step 1: Access Supabase Dashboard
1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Select your project: `ieugtoltckngbxreohcv`
3. Navigate to **Storage** in the left sidebar

### Step 2: Create Storage Buckets
Create the following buckets with the specified settings:

#### 1. Certificates Bucket
- **Bucket Name**: `certificates`
- **Public**: ✅ Yes (checked)
- **File Size Limit**: 10MB
- **Allowed MIME Types**: 
  - `application/pdf`
  - `image/jpeg`
  - `image/png`
  - `image/jpg`

#### 2. Profile Pictures Bucket
- **Bucket Name**: `profile-pictures`
- **Public**: ✅ Yes (checked)
- **File Size Limit**: 5MB
- **Allowed MIME Types**:
  - `image/jpeg`
  - `image/png`
  - `image/jpg`
  - `image/gif`

#### 3. Documents Bucket
- **Bucket Name**: `documents`
- **Public**: ✅ Yes (checked)
- **File Size Limit**: 10MB
- **Allowed MIME Types**:
  - `application/pdf`
  - `image/jpeg`
  - `image/png`
  - `image/jpg`

### Step 3: Configure RLS Policies

For each bucket, you need to set up Row Level Security policies:

#### Certificates Bucket Policies
```sql
-- Allow authenticated users to upload certificates
CREATE POLICY "Users can upload certificates" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'certificates' AND
  auth.role() = 'authenticated'
);

-- Allow users to view their own certificates
CREATE POLICY "Users can view own certificates" ON storage.objects
FOR SELECT USING (
  bucket_id = 'certificates' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Allow users to delete their own certificates
CREATE POLICY "Users can delete own certificates" ON storage.objects
FOR DELETE USING (
  bucket_id = 'certificates' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
```

#### Profile Pictures Bucket Policies
```sql
-- Allow authenticated users to upload profile pictures
CREATE POLICY "Users can upload profile pictures" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'profile-pictures' AND
  auth.role() = 'authenticated'
);

-- Allow users to view their own profile pictures
CREATE POLICY "Users can view own profile pictures" ON storage.objects
FOR SELECT USING (
  bucket_id = 'profile-pictures' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Allow users to delete their own profile pictures
CREATE POLICY "Users can delete own profile pictures" ON storage.objects
FOR DELETE USING (
  bucket_id = 'profile-pictures' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
```

#### Documents Bucket Policies
```sql
-- Allow authenticated users to upload documents
CREATE POLICY "Users can upload documents" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'documents' AND
  auth.role() = 'authenticated'
);

-- Allow users to view their own documents
CREATE POLICY "Users can view own documents" ON storage.objects
FOR SELECT USING (
  bucket_id = 'documents' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Allow users to delete their own documents
CREATE POLICY "Users can delete own documents" ON storage.objects
FOR DELETE USING (
  bucket_id = 'documents' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
```

## Testing the Setup

### 1. Test Backend Connection
```bash
cd backend
python test_supabase_connection.py
```

### 2. Test File Upload API
```bash
# Start the backend server
python main.py

# Test file upload (requires authentication)
curl -X POST "http://localhost:8000/api/upload/certificate" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@test_certificate.pdf"
```

### 3. Test Storage Buckets
```bash
# Test storage bucket setup
curl -X POST "http://localhost:8000/api/setup-storage" \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN"
```

## File Upload Features

### Supported File Types
- **Certificates**: PDF, JPEG, PNG, JPG (max 10MB)
- **Profile Pictures**: JPEG, PNG, JPG, GIF (max 5MB)
- **Documents**: PDF, JPEG, PNG, JPG (max 10MB)

### API Endpoints
- `POST /api/upload/certificate` - Upload certificate
- `POST /api/upload/profile-picture` - Upload profile picture
- `GET /api/files/my-files` - Get user's files
- `GET /api/files/{file_id}` - Get file info
- `DELETE /api/files/{file_id}` - Delete file
- `POST /api/setup-storage` - Setup storage buckets (admin only)

### File Storage Structure
```
uploads/
├── certificates/
│   └── {user_id}_{activity_id}_{uuid}.{ext}
├── profile_pictures/
│   └── {user_id}_{uuid}.{ext}
└── documents/
    └── {user_id}_{activity_id}_{uuid}.{ext}
```

## Troubleshooting

### Common Issues

1. **"Bucket not found" error**
   - Ensure buckets are created in Supabase dashboard
   - Check bucket names match exactly

2. **"Unauthorized" error**
   - Verify RLS policies are set up correctly
   - Check user authentication

3. **File upload fails**
   - Check file size limits
   - Verify file type is allowed
   - Ensure user is authenticated

4. **Database constraint errors**
   - Check if file_storage table exists
   - Verify table structure matches expectations

### Debug Commands
```bash
# Check database tables
python check_tables.py

# Check file storage table structure
python check_file_storage_table.py

# Test Supabase connection
python test_supabase_connection.py
```

## Security Considerations

1. **File Validation**: All uploaded files are validated for type and size
2. **User Isolation**: Users can only access their own files
3. **Authentication Required**: All upload endpoints require valid JWT tokens
4. **Local Backup**: Files are stored both in Supabase and locally
5. **Unique Filenames**: Generated UUIDs prevent filename conflicts

## Performance Optimization

1. **Connection Pooling**: Supabase client uses connection pooling
2. **Local Caching**: Files are cached locally for faster access
3. **Async Uploads**: File uploads are processed asynchronously
4. **Compression**: Large files are compressed before upload

## Next Steps

1. Complete the Supabase dashboard setup
2. Test file uploads through the API
3. Integrate with the frontend React application
4. Set up monitoring and logging
5. Configure backup and recovery procedures

---

**Note**: This setup provides a hybrid approach using both Supabase storage and local file storage for maximum reliability and performance.
