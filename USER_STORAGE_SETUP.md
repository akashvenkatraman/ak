# 🗄️ User Storage Setup Guide

## Overview
This guide will help you set up user-specific storage buckets in Supabase for the Smart Student Hub application. Each user will have their own isolated storage space for images and documents.

## 🎯 **What This Setup Provides**

### **Storage Buckets Created:**
1. **`user-images`** - General user images (10MB limit)
2. **`profile-pictures`** - User profile pictures (5MB limit)  
3. **`activity-documents`** - Activity-related documents (15MB limit)

### **User Isolation:**
- Each user has their own folder: `{user_id}/`
- Users can only access their own files
- Teachers can view their students' activity documents
- Secure file access with Row Level Security (RLS)

## 🚀 **Quick Setup**

### **Step 1: Configure Service Key**
Update your `config.py` with your Supabase service key:

```python
# In config.py
supabase_service_key: str = "your_actual_service_key_here"
```

**To get your service key:**
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Settings** → **API**
4. Copy the **service_role** key

### **Step 2: Run Storage Setup**
```bash
cd backend
python setup_user_storage.py
```

This will:
- ✅ Create all storage buckets
- ✅ Generate RLS policies
- ✅ Test the connection
- ✅ Provide next steps

### **Step 3: Apply RLS Policies**
The script will output SQL policies. Copy and run them in your Supabase SQL editor:

1. Go to **SQL Editor** in Supabase dashboard
2. Paste the generated policies
3. Click **Run**

## 📁 **Storage Structure**

```
Supabase Storage/
├── user-images/
│   └── {user_id}/
│       ├── {uuid}_image1.jpg
│       ├── {uuid}_image2.png
│       └── activities/
│           └── {activity_id}/
│               └── {uuid}_activity_image.jpg
├── profile-pictures/
│   └── {user_id}/
│       └── {uuid}_profile.jpg
└── activity-documents/
    └── {user_id}/
        └── activities/
            └── {activity_id}/
                ├── {uuid}_document.pdf
                └── {uuid}_certificate.jpg
```

## 🔐 **Security Features**

### **Row Level Security (RLS) Policies:**
- Users can only upload to their own folders
- Users can only view their own files
- Teachers can view their students' activity documents
- File type validation (images, PDFs, documents)
- File size limits enforced

### **File Validation:**
- **Images**: JPEG, PNG, GIF, WebP
- **Documents**: PDF, DOC, DOCX
- **Size Limits**: 5-15MB depending on bucket
- **Virus Scanning**: Built into Supabase

## 🛠️ **API Endpoints**

### **Upload Endpoints:**
```bash
# Upload user image
POST /api/storage/upload/user-image
Content-Type: multipart/form-data
- file: image file
- activity_id: optional

# Upload profile picture
POST /api/storage/upload/profile-picture
Content-Type: multipart/form-data
- file: image file

# Upload activity document
POST /api/storage/upload/activity-document
Content-Type: multipart/form-data
- file: document file
- activity_id: required
```

### **Retrieval Endpoints:**
```bash
# Get user's images
GET /api/storage/files/my-images

# Get user's documents
GET /api/storage/files/my-documents

# Get profile picture
GET /api/storage/files/profile-picture

# Get storage status
GET /api/storage/storage/status
```

### **Management Endpoints:**
```bash
# Delete file
DELETE /api/storage/files/delete
- file_path: path to file
- bucket_name: bucket name

# Get file info
GET /api/storage/files/info
- file_path: path to file
- bucket_name: bucket name
```

## 🧪 **Testing the Setup**

### **1. Test Storage Connection:**
```bash
cd backend
python -c "from setup_user_storage import SupabaseStorageSetup; setup = SupabaseStorageSetup(); print('✅ Connection:', setup.test_storage_connection())"
```

### **2. Test File Upload:**
```bash
# Start the backend server
python main.py

# Test upload (requires authentication)
curl -X POST "http://localhost:8000/api/storage/upload/user-image" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@test_image.jpg"
```

### **3. Test File Retrieval:**
```bash
curl -X GET "http://localhost:8000/api/storage/files/my-images" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔧 **Frontend Integration**

### **React Component Example:**
```typescript
// Upload component
const uploadImage = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('/api/storage/upload/user-image', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  return response.json();
};

// Display user images
const getUserImages = async () => {
  const response = await fetch('/api/storage/files/my-images', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.json();
};
```

## 📊 **Storage Monitoring**

### **Check Storage Usage:**
```bash
curl -X GET "http://localhost:8000/api/storage/storage/status" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "data": {
    "storage_usage": {
      "total_size_mb": 15.5,
      "user_images_count": 5,
      "profile_pictures_count": 1,
      "activity_documents_count": 3,
      "total_files": 9
    }
  }
}
```

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **"Service key not configured"**
   - Update `config.py` with your actual service key
   - Get it from Supabase dashboard → Settings → API

2. **"Bucket not found"**
   - Run the setup script: `python setup_user_storage.py`
   - Check bucket names in Supabase dashboard

3. **"Unauthorized" errors**
   - Verify RLS policies are applied
   - Check user authentication
   - Ensure JWT token is valid

4. **File upload fails**
   - Check file size limits
   - Verify file type is allowed
   - Ensure user is authenticated

### **Debug Commands:**
```bash
# Check storage connection
python -c "from app.services.storage_service import storage_service; print(storage_service.test_storage_connection())"

# List existing buckets
python -c "from setup_user_storage import SupabaseStorageSetup; setup = SupabaseStorageSetup(); setup.list_existing_buckets()"

# Test file upload
python -c "from app.services.storage_service import storage_service; result = storage_service.upload_user_image(1, b'test', 'test.jpg'); print(result)"
```

## 🔄 **Maintenance**

### **Regular Tasks:**
1. **Monitor storage usage** - Check for users approaching limits
2. **Clean up old files** - Remove unused files periodically
3. **Update policies** - Review and update RLS policies as needed
4. **Backup important files** - Ensure critical documents are backed up

### **Storage Limits:**
- **Per User**: No hard limit (monitor usage)
- **Per File**: 5-15MB depending on type
- **Total Project**: Depends on your Supabase plan

## 🎉 **Success Indicators**

You'll know the setup is working when:
- ✅ Storage buckets are created in Supabase dashboard
- ✅ RLS policies are active
- ✅ File uploads work through API
- ✅ Users can only access their own files
- ✅ Teachers can view student documents
- ✅ File validation works correctly

## 📞 **Support**

If you encounter issues:
1. Check the terminal output for error messages
2. Verify your Supabase credentials
3. Ensure all dependencies are installed
4. Check the Supabase dashboard for bucket status
5. Review the RLS policies in the SQL editor

---

**🎯 Once setup is complete, you'll have a fully functional user-specific storage system with proper security and isolation!**
