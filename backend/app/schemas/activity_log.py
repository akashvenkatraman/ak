from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.activity_log import ActivityLogType

class ActivityLogBase(BaseModel):
    activity_id: int
    log_type: ActivityLogType
    action: str
    details: Optional[Dict[str, Any]] = None
    target_user_id: Optional[int] = None

class ActivityLogCreate(ActivityLogBase):
    user_id: int

class ActivityLogResponse(ActivityLogBase):
    id: int
    user_id: int
    user_name: Optional[str] = None
    target_user_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class FileStorageBase(BaseModel):
    activity_id: int
    file_name: str
    original_name: str
    file_path: str
    file_size: int
    file_type: str
    file_extension: str
    is_certificate: bool = True

class FileStorageCreate(FileStorageBase):
    uploaded_by: int

class FileStorageResponse(FileStorageBase):
    id: int
    uploaded_by: int
    uploader_name: Optional[str] = None
    download_count: int = 0
    view_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class FileDownloadResponse(BaseModel):
    file_path: str
    file_name: str
    file_type: str
    file_size: int
    download_url: str

class ActivityWithFiles(BaseModel):
    id: int
    student_id: int
    student_name: Optional[str] = None
    title: str
    description: Optional[str] = None
    activity_type: str
    credits: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str
    files_count: int
    files: list[FileStorageResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ActivityLogSummary(BaseModel):
    total_logs: int
    logs_by_type: Dict[str, int]
    recent_logs: list[ActivityLogResponse]
    activity_stats: Dict[str, int]
