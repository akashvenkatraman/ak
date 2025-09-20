# Certificate Management Portal

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

## Project Structure

```
certificate-management-portal/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Authentication & database
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── hooks/        # Custom React hooks
│   │   ├── types/        # TypeScript type definitions
│   │   └── utils/        # Utility functions
│   └── package.json      # Node.js dependencies
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Supabase account (optional, can use SQLite for development)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `config.py` and update the settings
   - Set your Supabase URL and keys (or use SQLite for development)
   - Generate a secure secret key for JWT

5. Create the first admin user:
   ```bash
   python -c "
   from main import app
   from app.schemas.user import UserCreate
   from app.models.user import UserRole
   import requests
   
   # Start the server first with: uvicorn main:app --reload
   # Then run this to create admin
   admin_data = {
       'email': 'admin@example.com',
       'username': 'admin',
       'full_name': 'System Administrator',
       'password': 'admin123456',
       'role': 'admin'
   }
   response = requests.post('http://localhost:8000/auth/create-admin', json=admin_data)
   print(response.json())
   "
   ```

6. Start the development server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   # Create .env file with:
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_WS_URL=ws://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage

### Initial Setup
1. Create the first admin user using the backend setup instructions
2. Access the frontend at http://localhost:3000
3. Login with admin credentials
4. Approve teacher and student registrations
5. Allocate students to teachers

### User Registration Flow
1. Users register via the signup page (students and teachers only)
2. Admin reviews and approves/rejects registrations
3. Approved users can login and access their respective dashboards

### Activity Submission Flow
1. Students upload activity certificates and details
2. Teachers receive real-time notifications
3. Teachers review and approve/reject activities
4. Students see updated status and earned credits

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info
- `POST /auth/create-admin` - Create admin user

### Admin Endpoints
- `GET /admin/pending-users` - Get pending registrations
- `POST /admin/approve-user` - Approve/reject user
- `POST /admin/allocate-students` - Allocate students to teachers
- `GET /admin/allocations` - Get all allocations

### Teacher Endpoints
- `GET /teachers/dashboard` - Teacher dashboard stats
- `GET /teachers/students` - Get assigned students
- `GET /teachers/pending-activities` - Get pending activities
- `POST /teachers/approve-activity` - Approve/reject activity

### Student Endpoints
- `GET /students/dashboard` - Student dashboard stats
- `POST /students/activities` - Submit new activity
- `GET /students/activities` - Get student activities
- `PUT /students/activities/{id}` - Update activity

### WebSocket
- `WS /ws/{user_id}?token={jwt_token}` - Real-time notifications

## Development

### Adding New Features
1. Create database models in `backend/app/models/`
2. Define Pydantic schemas in `backend/app/schemas/`
3. Implement API routes in `backend/app/api/`
4. Add TypeScript types in `frontend/src/types/`
5. Create React components and pages
6. Update API services in `frontend/src/services/`

### Database Migrations
The application uses SQLAlchemy for database management. For production:
1. Set up Alembic for migrations
2. Create migration scripts for schema changes
3. Apply migrations to production database

## Deployment

### Backend Deployment
1. Use a production WSGI server like Gunicorn
2. Set up environment variables securely
3. Configure database connection for production
4. Set up reverse proxy with Nginx

### Frontend Deployment
1. Build the production bundle: `npm run build`
2. Serve static files with Nginx or CDN
3. Configure environment variables for production API URL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/docs`

## Security Considerations

- JWT tokens for secure authentication
- Role-based access control
- File upload validation
- SQL injection protection with SQLAlchemy ORM
- CORS configuration for frontend-backend communication
- Password hashing with bcrypt

