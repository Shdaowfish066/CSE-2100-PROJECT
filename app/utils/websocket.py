"""WebSocket utilities for real-time messaging.

Developer: Tahsan (2303133)
"""

from fastapi import WebSocket, status
from sqlalchemy.orm import Session
from app.models.m_2303133_message import Message
from app.models.m_2303147_user import User
from datetime import datetime
import json


class ConnectionManager:
    """Manages WebSocket connections for real-time messaging.
    
    Maintains active connections and broadcasts messages between users.
    Uses a format: {user_id: websocket} for tracking active users.
    """
    
    def __init__(self):
        # Structure: {user_id: websocket}
        self.active_connections: dict[int, WebSocket] = {}
    
    async def connect(self, user_id: int, websocket: WebSocket):
        """Accept a new WebSocket connection for a user."""
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        """Remove a user's WebSocket connection."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_personal_message(self, user_id: int, message: dict):
        """Send a message to a specific user if they're connected."""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception as e:
                print(f"Error sending message to user {user_id}: {e}")
                self.disconnect(user_id)
    
    async def broadcast_to_users(self, sender_id: int, recipient_id: int, message: dict):
        """Send a message to both sender and recipient."""
        await self.send_personal_message(sender_id, message)
        await self.send_personal_message(recipient_id, message)
    
    def is_user_online(self, user_id: int) -> bool:
        """Check if a user is currently online."""
        return user_id in self.active_connections


# Global connection manager instance
connection_manager = ConnectionManager()
