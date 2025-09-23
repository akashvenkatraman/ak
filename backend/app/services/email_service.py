from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import settings
import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import text

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    # fastapi-mail expects explicit STARTTLS/SSL settings in recent versions
    MAIL_STARTTLS=getattr(settings, "mail_starttls", settings.mail_tls),
    MAIL_SSL_TLS=getattr(settings, "mail_ssl_tls", settings.mail_ssl),
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs,
)

class EmailService:
    def __init__(self):
        self.fastmail = FastMail(conf)
    
    def generate_verification_code(self) -> str:
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))
    
    def generate_reset_token(self) -> str:
        """Generate a secure reset token"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    async def send_password_reset_email(self, email: str, verification_code: str, db: Session):
        """Send password reset verification code to user's email"""
        try:
            # Check if email is properly configured
            if (settings.mail_username == "test@gmail.com" or 
                settings.mail_password == "test_password"):
                # Store verification code in database but don't send email
                expires_at = datetime.utcnow() + timedelta(minutes=10)  # Code expires in 10 minutes
                
                db.execute(text("""
                    UPDATE users 
                    SET verification_code = :code, 
                        verification_expires = :expires
                    WHERE email = :email
                """), {
                    "code": verification_code,
                    "expires": expires_at,
                    "email": email
                })
                db.commit()
                
                print(f"🔧 EMAIL NOT CONFIGURED - Verification code for {email}: {verification_code}")
                return True
            
            # Store verification code in database with expiration
            expires_at = datetime.utcnow() + timedelta(minutes=10)  # Code expires in 10 minutes
            
            # Store in a simple way - you might want to create a separate table for this
            db.execute(text("""
                UPDATE users 
                SET verification_code = :code, 
                    verification_expires = :expires
                WHERE email = :email
            """), {
                "code": verification_code,
                "expires": expires_at,
                "email": email
            })
            db.commit()
            
            # Create email message
            message = MessageSchema(
                subject="Password Reset Verification Code",
                recipients=[email],
                body=f"""
                <html>
                <body>
                    <h2>Password Reset Request</h2>
                    <p>You have requested to reset your password for Smart Student Hub.</p>
                    <p>Your verification code is: <strong style="font-size: 24px; color: #007bff;">{verification_code}</strong></p>
                    <p>This code will expire in 10 minutes.</p>
                    <p>If you did not request this password reset, please ignore this email.</p>
                    <br>
                    <p>Best regards,<br>Smart Student Hub Team</p>
                </body>
                </html>
                """,
                subtype="html"
            )
            
            # Send email
            await self.fastmail.send_message(message)
            return True
            
        except Exception as e:
            print(f"Error sending password reset email: {e}")
            return False
    
    async def send_welcome_email(self, email: str, full_name: str):
        """Send welcome email to new user"""
        try:
            message = MessageSchema(
                subject="Welcome to Smart Student Hub!",
                recipients=[email],
                body=f"""
                <html>
                <body>
                    <h2>Welcome to Smart Student Hub, {full_name}!</h2>
                    <p>Your account has been successfully created.</p>
                    <p>You can now access all the features of our platform:</p>
                    <ul>
                        <li>📚 Course Management</li>
                        <li>📊 Progress Tracking</li>
                        <li>👥 Student Collaboration</li>
                        <li>📝 Assignment Submission</li>
                        <li>💬 Discussion Forums</li>
                    </ul>
                    <p>Get started by logging in to your account!</p>
                    <br>
                    <p>Best regards,<br>Smart Student Hub Team</p>
                </body>
                </html>
                """,
                subtype="html"
            )
            
            await self.fastmail.send_message(message)
            return True
            
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            return False
    
    def verify_code(self, email: str, code: str, db: Session) -> bool:
        """Verify the password reset code"""
        try:
            result = db.execute(text("""
                SELECT verification_code, verification_expires 
                FROM users 
                WHERE email = :email
            """), {"email": email}).fetchone()
            
            if not result:
                return False
            
            stored_code, expires_at = result
            
            # Check if code matches and hasn't expired
            if stored_code == code and expires_at > datetime.utcnow():
                # Clear the verification code after successful verification
                db.execute(text("""
                    UPDATE users 
                    SET verification_code = NULL, 
                        verification_expires = NULL
                    WHERE email = :email
                """), {"email": email})
                db.commit()
                return True
            
            return False
            
        except Exception as e:
            print(f"Error verifying code: {e}")
            return False

# Create global instance
email_service = EmailService()
