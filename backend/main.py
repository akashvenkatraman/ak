from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import create_tables, Base, engine
from app.api import auth, admin, students, teachers, websocket, health, files, activity_logs, notifications
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

# Create uploads directory
os.makedirs("uploads/certificates", exist_ok=True)

# Mount static files for uploaded certificates
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
