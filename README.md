# Smart Student Hub 🎓

A comprehensive centralized certificate management system for educational institutions with role-based access control for administrators, teachers, and students.

## Features

### For Students
- **Dynamic Dashboard**: Real-time updates on academic performance, attendance, and credit-based activities
- **Activity Tracker**: Upload participation records for seminars, conferences, online courses (MOOCs), internships, and extracurricular activities
- **File Upload**: Submit certificates and supporting documents
- **Progress Tracking**: Monitor approval status of submitted activities
- **Credit Management**: Track earned credits from approved activities

### For Teachers
- **Student Management**: View assigned students and their activities
- **Review System**: Approve or reject student activity submissions
- **Real-time Notifications**: Get notified when students upload new activities
- **Dashboard Analytics**: Overview of pending reviews and approval statistics
- **Document Review**: View and download student certificates

### For Administrators
- **User Management**: Approve/reject teacher and student registrations
- **Student Allocation**: Assign students to teachers for supervision
- **System Overview**: Monitor platform usage and statistics
- **Role Management**: Manage user roles and permissions

## Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Supabase**: Database and authentication
- **WebSockets**: Real-time notifications
- **JWT**: Secure authentication tokens

### Frontend
- **React**: Modern UI library with TypeScript
- **Material-UI**: Professional component library
- **Axios**: HTTP client for API communication
- **React Router**: Client-side routing
- **Recharts**: Data visualization

## Quick Setup

See `tobedownload.txt` for a complete setup guide!

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL

### Backend Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## License

This project is licensed under the MIT License.
