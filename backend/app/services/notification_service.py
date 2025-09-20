from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationType
from app.models.user import User, TeacherStudentAllocation
from typing import List, Optional

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(
        self,
        user_id: int,
        notification_type: NotificationType,
        title: str,
        message: str,
        related_activity_id: Optional[int] = None,
        related_user_id: Optional[int] = None
    ) -> Notification:
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=message,
            related_activity_id=related_activity_id,
            related_user_id=related_user_id
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def notify_teachers_of_activity_submission(
        self,
        activity_id: int,
        student_id: int,
        activity_title: str,
        student_name: str
    ) -> List[Notification]:
        """Notify all teachers assigned to a student when they submit an activity"""
        # Get all teachers assigned to this student
        allocations = self.db.query(TeacherStudentAllocation).filter(
            TeacherStudentAllocation.student_id == student_id
        ).all()
        
        notifications = []
        for allocation in allocations:
            teacher = self.db.query(User).filter(User.id == allocation.teacher_id).first()
            if teacher:
                notification = self.create_notification(
                    user_id=teacher.id,
                    notification_type=NotificationType.ACTIVITY_SUBMITTED,
                    title="New Activity Submission",
                    message=f"Student {student_name} has submitted a new activity: '{activity_title}'",
                    related_activity_id=activity_id,
                    related_user_id=student_id
                )
                notifications.append(notification)
        
        return notifications
    
    def notify_student_of_activity_decision(
        self,
        activity_id: int,
        student_id: int,
        activity_title: str,
        decision: str,
        teacher_name: str,
        comments: Optional[str] = None
    ) -> Notification:
        """Notify student when their activity is approved or rejected"""
        notification_type = (
            NotificationType.ACTIVITY_APPROVED if decision == "approved" 
            else NotificationType.ACTIVITY_REJECTED
        )
        
        title = f"Activity {decision.title()}"
        message = f"Your activity '{activity_title}' has been {decision} by {teacher_name}"
        if comments:
            message += f". Comments: {comments}"
        
        return self.create_notification(
            user_id=student_id,
            notification_type=notification_type,
            title=title,
            message=message,
            related_activity_id=activity_id
        )
    
    def get_user_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a user"""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
        
        return query.order_by(Notification.created_at.desc()).limit(limit).all()
    
    def mark_notification_as_read(self, notification_id: int, user_id: int) -> bool:
        """Mark a notification as read"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if notification:
            notification.is_read = True
            from datetime import datetime
            notification.read_at = datetime.utcnow()
            self.db.commit()
            return True
        
        return False
    
    def mark_all_notifications_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user"""
        from datetime import datetime
        updated = self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({
            "is_read": True,
            "read_at": datetime.utcnow()
        })
        self.db.commit()
        return updated
