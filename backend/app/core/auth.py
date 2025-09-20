from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.schemas.user import TokenData
from config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        
        if username is None or user_id is None:
            raise credentials_exception
            
        token_data = TokenData(username=username, user_id=user_id, role=role)
        return token_data
    except JWTError:
        raise credentials_exception

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user"""
    token = credentials.credentials
    token_data = verify_token(token)
    
    # Use raw SQL to avoid enum issues
    try:
        from sqlalchemy import text
        result = db.execute(text("SELECT * FROM users WHERE id = :user_id"), 
                          {"user_id": token_data.user_id}).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Create User object manually with all profile fields
        user = User(
            id=result.id,
            email=result.email,
            username=result.username,
            full_name=result.full_name,
            hashed_password=result.hashed_password,
            role=result.role.lower(),  # Convert to lowercase for enum compatibility
            status=result.status.lower(),  # Convert to lowercase for enum compatibility
            is_active=result.is_active,
            phone_number=result.phone_number,
            department=result.department,
            student_id=result.student_id,
            employee_id=result.employee_id,
            performance_score=result.performance_score,
            total_credits_earned=result.total_credits_earned,
            profile_picture=result.profile_picture,
            bio=result.bio,
            date_of_birth=result.date_of_birth,
            address=result.address,
            city=result.city,
            state=result.state,
            country=result.country,
            postal_code=result.postal_code,
            linkedin_url=result.linkedin_url,
            twitter_url=result.twitter_url,
            website_url=result.website_url,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
    except Exception as e:
        print(f"Auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if user.status.upper() != UserStatus.APPROVED.value.upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not approved"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user"""
    return current_user

def require_role(required_roles: list[UserRole]):
    """Decorator to require specific user roles"""
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

# Role-specific dependencies
def get_admin_user(current_user: User = Depends(require_role([UserRole.ADMIN]))) -> User:
    return current_user

def get_teacher_user(current_user: User = Depends(require_role([UserRole.TEACHER]))) -> User:
    return current_user

def get_student_user(current_user: User = Depends(require_role([UserRole.STUDENT]))) -> User:
    return current_user

def get_teacher_or_admin_user(current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN]))) -> User:
    return current_user
