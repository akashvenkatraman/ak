# 🎓 Smart Student Hub - Quick Start Guide

## 🚀 READY TO RUN!

Your project is fully configured and ready to use. Here's how to get started:

## ⚡ Quick Start (Choose One)

### Option 1: One-Click Start
**Double-click `start_all.bat`** - This will start both servers automatically!

### Option 2: Manual Start
1. **Backend**: Double-click `start_backend.bat`
2. **Frontend**: Double-click `start_frontend.bat`

## 🌐 Access Your Application

- **Main App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Backend API**: http://localhost:8000

## 🔐 Login Credentials

**Admin Account:**
- Email: `admin@example.com`
- Password: `admin123456`

## 📋 What You Can Do

1. **Login as Admin** - Manage users and system
2. **Register Students/Teachers** - Create new accounts
3. **Approve Users** - Review and approve registrations
4. **Upload Activities** - Students can submit certificates
5. **Review Submissions** - Teachers can approve/reject activities

## 🛠️ Project Features

### ✅ Student Features
- Upload certificates and activities
- Track progress and credits
- View dashboard with real-time updates

### ✅ Teacher Features
- Review student submissions
- Approve/reject activities
- Manage assigned students

### ✅ Admin Features
- User management
- System overview
- Role assignments

## 🔧 If Something Goes Wrong

1. **Backend not starting?**
   - Check if port 8000 is free
   - Run `cd backend && venv\Scripts\activate && uvicorn main:app --reload`

2. **Frontend not starting?**
   - Check if port 3000 is free
   - Run `cd frontend && npm start`

3. **Database issues?**
   - Check `.env` file in backend folder
   - Verify Supabase credentials

## 📁 File Structure

```
smartstudenthub/
├── start_all.bat          ← Double-click this to start everything!
├── start_backend.bat      ← Backend only
├── start_frontend.bat     ← Frontend only
├── backend/               ← FastAPI server
├── frontend/              ← React app
└── SETUP_INSTRUCTIONS.md  ← Detailed setup guide
```

## 🎉 You're All Set!

Your Smart Student Hub is ready to use. Start with the admin account to explore all features!

**Happy Learning! 🎓**
