from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verify_token
from app.services.notification import NotificationService
import json

router = APIRouter()

# Global notification service instance
notification_services: dict[int, NotificationService] = {}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, token: str = Query(...), db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time notifications"""
    
    try:
        # Verify token
        token_data = verify_token(token)
        if token_data.user_id != user_id:
            await websocket.close(code=1008, reason="Invalid token")
            return
        
        # Create notification service if not exists
        if user_id not in notification_services:
            notification_services[user_id] = NotificationService(db)
        
        notification_service = notification_services[user_id]
        
        # Connect user
        await notification_service.connect(user_id, websocket)
        
        try:
            while True:
                # Keep connection alive and handle incoming messages
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                
        except WebSocketDisconnect:
            notification_service.disconnect(user_id)
            if user_id in notification_services:
                del notification_services[user_id]
    
    except Exception as e:
        await websocket.close(code=1011, reason=f"Server error: {str(e)}")

def get_notification_service(db: Session) -> NotificationService:
    """Get or create notification service instance"""
    # For simplicity, create a new instance each time
    # In production, you might want to use a singleton pattern
    return NotificationService(db)

