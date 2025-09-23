from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import create_tables, Base, engine
from app.api import auth, admin, students, teachers, websocket, health, files, activity_logs, notifications, profile, oauth, file_uploads, erp_integration, user_storage
from export_endpoints import router as export_router
from analytics_endpoints import router as analytics_router
from sample_data_endpoints import router as sample_data_router
from config import settings
import os

# Import models to register them with SQLAlchemy
from app.models import user, activity, activity_log, notification

# Create FastAPI app
app = FastAPI(
    title="Certificate Management Portal",
    description="A centralized certificate management system for educational institutions",
    version="1.0.0",
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directories
os.makedirs("uploads/certificates", exist_ok=True)
os.makedirs("uploads/profile_pictures", exist_ok=True)

# Mount static files for uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(websocket.router)
app.include_router(files.router)
app.include_router(activity_logs.router)
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
app.include_router(profile.router, tags=["profile"])
app.include_router(oauth.router, prefix="/api", tags=["oauth"])
app.include_router(file_uploads.router, prefix="/api", tags=["file-uploads"])
app.include_router(user_storage.router, prefix="/api/storage", tags=["user-storage"])
app.include_router(erp_integration.router, tags=["ERP Integration"])
app.include_router(export_router, tags=["Data Export"])
app.include_router(analytics_router, tags=["Analytics"])
app.include_router(sample_data_router, tags=["Sample Data"])

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    # Create all tables
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Certificate Management Portal API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "status": "active"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
