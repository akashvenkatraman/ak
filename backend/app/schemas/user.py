from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole, UserStatus

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: UserRole
    phone_number: Optional[str] = None
    department: Optional[str] = None
    student_id: Optional[str] = None
    employee_id: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    student_id: Optional[str] = None
    employee_id: Optional[str] = None

class UserInDB(UserBase):
    id: int
    status: UserStatus
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    status: UserStatus
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[UserRole] = None

class UserApproval(BaseModel):
    user_id: int
    status: UserStatus
    comments: Optional[str] = None

class TeacherStudentAllocationCreate(BaseModel):
    teacher_id: int
    student_ids: List[int]

class TeacherStudentAllocationResponse(BaseModel):
    id: int
    teacher_id: int
    student_id: int
    teacher_name: str
    student_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

