# 🚀 Supabase Setup Guide for Certificate Management Portal

## 📋 **Prerequisites**

1. **Supabase Project**: You have a Supabase project at `https://ieugtoltckngbxreohcv.supabase.co`
2. **JWT Secret**: Your JWT secret is configured
3. **Database Password**: You need your Supabase database password

## 🔧 **Step 1: Get Supabase Credentials**

### **Get Database Password:**
1. Go to your Supabase dashboard: https://supabase.com/dashboard
2. Select your project
3. Go to **Settings** → **Database**
4. Copy the **Connection string** or **Password**
5. The format should be: `postgresql://postgres:[PASSWORD]@db.ieugtoltckngbxreohcv.supabase.co:5432/postgres`

### **Get API Keys:**
1. Go to **Settings** → **API**
2. Copy the **anon public** key
3. Copy the **service_role** key (for admin operations)

## 🔧 **Step 2: Configure Environment Variables**

Create a `.env` file in the `backend` directory:

```bash
# Supabase Configuration
SUPABASE_URL=https://ieugtoltckngbxreohcv.supabase.co
SUPABASE_KEY=your_anon_public_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here

# Database Configuration
DATABASE_PASSWORD=your_database_password_here

# JWT Configuration (already set)
SECRET_KEY=Dkq5f+z+8bsnHu+Dqa2fZSncaCGvC1dgYzFITE773w6H1IX94GiPk7WYQNlYGcTEz9Cz00JEz+RwlEig7/umGA==

# Application Configuration
DEBUG=True
HOST=localhost
PORT=8000
```

## 🔧 **Step 3: Install Dependencies**

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt
```

## 🔧 **Step 4: Run Setup Script**

```bash
# Run the automated setup
python setup_supabase.py
```

This script will:
- ✅ Test database connection
- ✅ Create all required tables
- ✅ Create admin user
- ✅ Verify everything is working

## 🔧 **Step 5: Start the Application**

### **Backend Server:**
```bash
# In backend directory
uvicorn main:app --reload
```

### **Frontend Server:**
```bash
# In frontend directory
npm start
```

## 🔧 **Step 6: Test the Application**

1. **Open**: http://localhost:3000
2. **Login as Admin**:
   - Email: `admin@example.com`
   - Password: `admin123456`
3. **Register Test Users**:
   - Go to `/register`
   - Create student and teacher accounts
4. **Approve Users**:
   - As admin, go to "Review Pending Users"
   - Approve the test accounts
5. **Test User Login**:
   - Logout as admin
   - Login with approved user credentials

## 🗄️ **Database Schema**

The setup script will create these tables in your Supabase database:

- **users**: User accounts (admin, teacher, student)
- **activities**: Student activity submissions
- **teacher_student_associations**: Student-teacher assignments

## 🔐 **Security Notes**

- **JWT Secret**: Already configured with your provided key
- **Database**: Uses Supabase PostgreSQL with proper authentication
- **File Uploads**: Stored in Supabase Storage (configured in main.py)
- **CORS**: Configured for localhost development

## 🚨 **Troubleshooting**

### **Connection Issues:**
- Verify your database password is correct
- Check if your Supabase project is active
- Ensure your IP is whitelisted in Supabase

### **Table Creation Issues:**
- Check database permissions
- Verify the connection string format
- Run the setup script again

### **Authentication Issues:**
- Verify JWT secret is correct
- Check if admin user was created successfully
- Clear browser cache and try again

## 📞 **Support**

If you encounter any issues:
1. Check the terminal output for error messages
2. Verify your Supabase credentials
3. Ensure all dependencies are installed
4. Try running the setup script again

---

**🎉 Once setup is complete, you'll have a fully functional Certificate Management Portal with Supabase backend!**





