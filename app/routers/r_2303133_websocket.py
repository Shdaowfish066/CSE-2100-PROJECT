"""WebSocket endpoints for real-time messaging.

Developer: Tahsan (2303133)
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Query
from sqlalchemy.orm import Session, sessionmaker
from app.database import engine
from app.models.m_2303133_message import Message
from app.models.m_2303147_user import User
from app.utils.websocket import connection_manager
from datetime import datetime
import json


router = APIRouter(prefix="/ws", tags=["websocket"])


@router.websocket("/chat/{other_user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    other_user_id: int,
    token: str = Query(...)
):
    """WebSocket endpoint for real-time messaging between two users.
    
    Connect to: ws://localhost:8000/ws/chat/{other_user_id}?token={your_token}
    
    Message format (send):
    {"content": "your message here"}
    
    Message format (receive):
    {
        "type": "message",
        "sender_id": 1,
        "recipient_id": 2,
        "content": "message content",
        "created_at": "2026-02-18T10:30:00",
        "is_read": false
    }
    """
    
    # Create a new database session for this WebSocket connection
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Verify token and get current user
    from app.utils.auth import decode_access_token
    try:
        payload = decode_access_token(token)
        if not payload:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            db.close()
            return
        current_user_id = int(payload.get("sub"))
        if not current_user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            db.close()
            return
    except Exception as e:
        print(f"Token decode error: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        db.close()
        return
    
    # Verify the other user exists
    other_user = db.query(User).filter(User.id == other_user_id).first()
    if not other_user:
        print(f"Other user {other_user_id} not found")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        db.close()
        return
    
    print(f"User {current_user_id} connecting to chat with user {other_user_id}")
    
    # Connect the user
    await connection_manager.connect(current_user_id, websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            content = message_data.get("content", "").strip()
            
            if not content:
                continue
            
            print(f"Message from {current_user_id} to {other_user_id}: {content}")
            
            # Save message to database
            message = Message(
                sender_id=current_user_id,
                recipient_id=other_user_id,
                content=content,
                created_at=datetime.utcnow(),
                is_read=False
            )
            db.add(message)
            db.commit()
            db.refresh(message)
            
            print(f"Message saved to DB with ID {message.id}")
            
            # Prepare response
            response = {
                "type": "message",
                "sender_id": message.sender_id,
                "recipient_id": message.recipient_id,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
                "is_read": message.is_read,
                "id": message.id
            }
            
            # Send to both users
            await connection_manager.broadcast_to_users(
                current_user_id,
                other_user_id,
                response
            )
            
    except WebSocketDisconnect:
        print(f"User {current_user_id} disconnected")
        connection_manager.disconnect(current_user_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        connection_manager.disconnect(current_user_id)
        try:
            await websocket.close(code=status.WS_1011_SERVER_ERROR)
        except:
            pass
    finally:
        db.close()
