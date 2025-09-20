from authlib.integrations.httpx_client import OAuth2Session
from config import settings
import httpx
from typing import Optional, Dict, Any
from app.core.database import SessionLocal
from app.models.user import User
from app.core.auth import create_access_token, get_password_hash
from sqlalchemy.orm import Session
from app.models.user import UserRole

class GoogleOAuthService:
    def __init__(self):
        self.client_id = settings.google_client_id
        self.client_secret = settings.google_client_secret
        self.redirect_uri = settings.google_redirect_uri
        self.authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    def get_authorization_url(self) -> str:
        """Get Google OAuth authorization URL"""
        # Check if Google OAuth is properly configured
        if (self.client_id == "123456789-abcdefghijklmnop.apps.googleusercontent.com" or 
            self.client_secret == "GOCSPX-abcdefghijklmnop"):
            raise Exception("Google OAuth not configured. Please set up Google OAuth credentials in config.py")
        
        oauth = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=["openid", "email", "profile"]
        )
        
        authorization_url, state = oauth.authorization_url(
            self.authorization_base_url,
            access_type="offline",
            prompt="select_account"
        )
        
        return authorization_url
    
    async def get_user_info(self, authorization_code: str) -> Optional[Dict[str, Any]]:
        """Get user information from Google using authorization code"""
        try:
            oauth = OAuth2Session(
                client_id=self.client_id,
                redirect_uri=self.redirect_uri
            )
            
            # Exchange authorization code for access token
            token = oauth.fetch_token(
                self.token_url,
                authorization_response=authorization_code,
                client_secret=self.client_secret
            )
            
            # Get user info from Google
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.user_info_url,
                    headers={"Authorization": f"Bearer {token['access_token']}"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Error getting user info: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"Error in Google OAuth: {e}")
            return None
    
    def create_or_get_user(self, google_user_info: Dict[str, Any], db: Session) -> Optional[User]:
        """Create new user or get existing user from Google OAuth data"""
        try:
            email = google_user_info.get("email")
            if not email:
                return None
            
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == email).first()
            
            if existing_user:
                # Update existing user with Google info if needed
                if not existing_user.profile_picture and google_user_info.get("picture"):
                    existing_user.profile_picture = google_user_info["picture"]
                if not existing_user.full_name and google_user_info.get("name"):
                    existing_user.full_name = google_user_info["name"]
                db.commit()
                return existing_user
            
            # Create new user
            username = email.split("@")[0]  # Use email prefix as username
            # Ensure username is unique
            counter = 1
            original_username = username
            while db.query(User).filter(User.username == username).first():
                username = f"{original_username}{counter}"
                counter += 1
            
            # Generate a random password for OAuth users
            random_password = f"oauth_{google_user_info.get('id', 'user')}"
            
            new_user = User(
                email=email,
                username=username,
                full_name=google_user_info.get("name", ""),
                hashed_password=get_password_hash(random_password),
                role=UserRole.student,  # Default role for OAuth users
                status="approved",  # Auto-approve OAuth users
                profile_picture=google_user_info.get("picture"),
                is_oauth_user=True  # Mark as OAuth user
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return new_user
            
        except Exception as e:
            print(f"Error creating/getting user: {e}")
            db.rollback()
            return None
    
    async def authenticate_user(self, authorization_code: str) -> Optional[Dict[str, Any]]:
        """Complete OAuth authentication and return user data with token"""
        try:
            # Get user info from Google
            google_user_info = await self.get_user_info(authorization_code)
            if not google_user_info:
                return None
            
            # Create or get user from database
            db = SessionLocal()
            try:
                user = self.create_or_get_user(google_user_info, db)
                if not user:
                    return None
                
                # Create access token
                access_token = create_access_token(data={"sub": user.username})
                
                # Convert user to dict for response
                user_dict = {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "role": user.role,
                    "status": user.status,
                    "phone_number": user.phone_number,
                    "department": user.department,
                    "student_id": user.student_id,
                    "employee_id": user.employee_id,
                    "performance_score": user.performance_score,
                    "total_credits_earned": user.total_credits_earned,
                    "profile_picture": user.profile_picture,
                    "bio": user.bio,
                    "date_of_birth": user.date_of_birth,
                    "address": user.address,
                    "city": user.city,
                    "state": user.state,
                    "country": user.country,
                    "postal_code": user.postal_code,
                    "linkedin_url": user.linkedin_url,
                    "twitter_url": user.twitter_url,
                    "website_url": user.website_url,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                }
                
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user": user_dict
                }
                
            finally:
                db.close()
                
        except Exception as e:
            print(f"Error in OAuth authentication: {e}")
            return None

# Create global instance
google_oauth_service = GoogleOAuthService()
