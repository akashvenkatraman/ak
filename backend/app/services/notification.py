from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.activity import Activity
import json
from datetime import datetime

class NotificationService:
    """Service for handling real-time notifications"""
    
    def __init__(self, db: Session):
        self.db = db
        self.active_connections: Dict[int, Any] = {}  # user_id -> websocket connection
    
    async def connect(self, user_id: int, websocket):
        """Connect a user to the notification service"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        """Disconnect a user from the notification service"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_personal_notification(self, user_id: int, message: dict):
        """Send notification to a specific user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
            except:
                # Connection is broken, remove it
                self.disconnect(user_id)
    
    async def notify_teachers_new_submission(self, activity: Activity):
        """Notify teachers when a student submits a new activity"""
        from app.models.user import TeacherStudentAllocation
        
        # Find teachers assigned to this student
        allocations = self.db.query(TeacherStudentAllocation).filter(
            TeacherStudentAllocation.student_id == activity.student_id
        ).all()
        
        # Get student info
        student = self.db.query(User).filter(User.id == activity.student_id).first()
        
        for allocation in allocations:
            message = {
                "type": "new_submission",
                "title": "New Activity Submission",
                "message": f"{student.full_name} submitted a new activity: {activity.title}",
                "activity_id": activity.id,
                "student_name": student.full_name,
                "activity_title": activity.title,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.send_personal_notification(allocation.teacher_id, message)
    
    async def notify_student_approval_status(self, activity: Activity, approval_status: str, teacher_name: str, comments: str = None):
        """Notify student when their activity is approved/rejected"""
        message = {
            "type": "approval_status",
            "title": f"Activity {approval_status.title()}",
            "message": f"Your activity '{activity.title}' has been {approval_status} by {teacher_name}",
            "activity_id": activity.id,
            "status": approval_status,
            "teacher_name": teacher_name,
            "comments": comments,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_personal_notification(activity.student_id, message)
    
    async def broadcast_to_role(self, role: UserRole, message: dict):
        """Broadcast message to all users with a specific role"""
        users = self.db.query(User).filter(User.role == role).all()
        for user in users:
            await self.send_personal_notification(user.id, message)

