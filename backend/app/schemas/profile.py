from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Union
from datetime import datetime
from app.models.user import UserRole

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    website_url: Optional[str] = None
    profile_picture: Optional[str] = None
    performance_score: Optional[int] = None
    total_credits_earned: Optional[int] = None
    
    @validator('linkedin_url', 'twitter_url', 'website_url')
    def validate_urls(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v

class ProfileResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    role: Union[UserRole, str]
    status: str
    phone_number: Optional[str] = None
    department: Optional[str] = None
    student_id: Optional[str] = None
    employee_id: Optional[str] = None
    performance_score: Optional[int] = None
    total_credits_earned: Optional[int] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    website_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

class ProfilePictureResponse(BaseModel):
    profile_picture: str
    message: str
