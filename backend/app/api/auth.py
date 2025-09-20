from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_user
)
from app.models.user import User, UserRole, UserStatus
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (student or teacher)"""
    
    try:
        from sqlalchemy import text
        
        # Check if user already exists using raw SQL
        email_check = db.execute(text("SELECT id FROM users WHERE email = :email"), 
                               {"email": user_data.email}).fetchone()
        if email_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        username_check = db.execute(text("SELECT id FROM users WHERE username = :username"), 
                                  {"username": user_data.username}).fetchone()
        if username_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Validate role (only students and teachers can self-register)
        if user_data.role not in ["student", "teacher"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role. Only students and teachers can register"
            )
        
        # Create new user using raw SQL to avoid enum issues
        hashed_password = get_password_hash(user_data.password)
        
        # Use raw connection to avoid ORM issues
        from app.core.database import engine
        with engine.begin() as conn:
            result = conn.execute(text("""
                INSERT INTO users (email, username, full_name, hashed_password, role, status, is_active, phone_number, department, student_id, employee_id, created_at)
                VALUES (:email, :username, :full_name, :hashed_password, :role, :status, :is_active, :phone_number, :department, :student_id, :employee_id, NOW())
                RETURNING id, email, username, full_name, role, status, is_active, phone_number, department, student_id, employee_id, created_at, updated_at
            """), {
                "email": user_data.email,
                "username": user_data.username,
                "full_name": user_data.full_name,
                "hashed_password": hashed_password,
                "role": user_data.role.upper(),  # Ensure uppercase for database constraint
                "status": "PENDING",  # Ensure uppercase for database constraint
                "is_active": True,
                "phone_number": user_data.phone_number,
                "department": user_data.department,
                "student_id": user_data.student_id,
                "employee_id": user_data.employee_id
            })
            
            user_row = result.fetchone()
        
        # Create User object for response with all profile fields
        db_user = User(
            id=user_row.id,
            email=user_row.email,
            username=user_row.username,
            full_name=user_row.full_name,
            hashed_password=None,  # Don't return hashed password
            role=user_row.role.lower(),  # Convert to lowercase for enum compatibility
            status=user_row.status.lower(),  # Convert to lowercase for enum compatibility
            is_active=user_row.is_active,
            phone_number=user_row.phone_number,
            department=user_row.department,
            student_id=user_row.student_id,
            employee_id=user_row.employee_id,
            performance_score=user_row.performance_score,
            total_credits_earned=user_row.total_credits_earned,
            profile_picture=user_row.profile_picture,
            bio=user_row.bio,
            date_of_birth=user_row.date_of_birth,
            address=user_row.address,
            city=user_row.city,
            state=user_row.state,
            country=user_row.country,
            postal_code=user_row.postal_code,
            linkedin_url=user_row.linkedin_url,
            twitter_url=user_row.twitter_url,
            website_url=user_row.website_url,
            created_at=user_row.created_at,
            updated_at=user_row.updated_at
        )
        
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    
    try:
        # Find user by username using raw SQL to avoid enum issues
        from sqlalchemy import text
        result = db.execute(text("SELECT * FROM users WHERE username = :username"), 
                          {"username": user_credentials.username}).fetchone()
        
        if not result:
            user = None
        else:
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
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. Please try again."
        )
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.status.upper() != UserStatus.APPROVED.value.upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is pending approval or has been rejected"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "role": user.role  # role is already a string
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible token endpoint"""
    user_credentials = UserLogin(username=form_data.username, password=form_data.password)
    return login(user_credentials, db)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/create-admin")
def create_admin_user(admin_data: UserCreate, db: Session = Depends(get_db)):
    """Create the first admin user - should be called only once during setup"""
    
    # Check if any admin exists
    existing_admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin user already exists"
        )
    
    # Force role to be admin
    admin_data.role = UserRole.ADMIN
    
    # Check if user already exists
    if db.query(User).filter(User.email == admin_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if db.query(User).filter(User.username == admin_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create admin user
    hashed_password = get_password_hash(admin_data.password)
    admin_user = User(
        email=admin_data.email,
        username=admin_data.username,
        full_name=admin_data.full_name,
        hashed_password=hashed_password,
        role=UserRole.ADMIN,
        phone_number=admin_data.phone_number,
        department=admin_data.department,
        status=UserStatus.APPROVED,  # Admin is auto-approved
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    return {"message": "Admin user created successfully", "user_id": admin_user.id}
