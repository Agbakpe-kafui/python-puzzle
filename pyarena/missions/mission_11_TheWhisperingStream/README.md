# 🌊 Mission 11: The Whispering Stream

**Status**: Advanced
**Difficulty**: Advanced
**Focus**: WebSockets & Real-time Communication

---

## 🎯 Mission Objective

Open channels to the Stream! Implement real-time bidirectional communication using WebSockets for live updates, notifications, and interactive features.

---

## 📚 What You'll Learn

- WebSocket protocol fundamentals
- FastAPI WebSocket support
- Real-time event broadcasting
- Connection management
- Client-side WebSocket handling
- Pub/Sub patterns
- Presence tracking

---

## ✅ Tasks

### 1. Create WebSocket Manager

Create `app/websocket_manager.py`:

```python
"""
WebSocket Connection Manager
Handles multiple WebSocket connections and broadcasting
"""

from typing import List, Dict
from fastapi import WebSocket
from datetime import datetime
import json


class ConnectionManager:
    """
    TODO: Implement WebSocket connection manager
    - Track active connections
    - Broadcast messages to all clients
    - Send messages to specific clients
    - Handle disconnections gracefully
    """

    def __init__(self):
        # Dict of user_id -> List[WebSocket]
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept and register new connection"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        """Remove connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        """Send message to specific user"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)

    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        for user_connections in self.active_connections.values():
            for connection in user_connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error broadcasting: {e}")

    def get_active_users(self) -> List[int]:
        """Get list of currently connected user IDs"""
        return list(self.active_connections.keys())


manager = ConnectionManager()
```

### 2. Create WebSocket Endpoints

Add to `app/routers/websocket.py`:

```python
"""
WebSocket Routes
Real-time communication endpoints
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.websocket_manager import manager
from app.utils.auth_utils import get_current_user
from app.models import User
import json

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int
):
    """
    TODO: Main WebSocket endpoint
    - Accept connection
    - Handle incoming messages
    - Broadcast to other users
    - Handle disconnection
    """
    await manager.connect(websocket, user_id)

    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "connection",
            "message": f"Welcome! You are connected as user {user_id}",
            "timestamp": datetime.utcnow().isoformat()
        }, user_id)

        # Broadcast user joined
        await manager.broadcast({
            "type": "user_joined",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Listen for messages
        while True:
            data = await websocket.receive_json()

            # Handle different message types
            if data.get("type") == "chat":
                await manager.broadcast({
                    "type": "chat",
                    "user_id": user_id,
                    "message": data.get("message"),
                    "timestamp": datetime.utcnow().isoformat()
                })

            elif data.get("type") == "typing":
                await manager.broadcast({
                    "type": "typing",
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast({
            "type": "user_left",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })


@router.websocket("/ws/notifications/{user_id}")
async def notification_stream(
    websocket: WebSocket,
    user_id: int
):
    """
    TODO: Notification stream WebSocket
    - Send real-time notifications to user
    - Mission completions
    - Achievement unlocks
    - System announcements
    """
    await manager.connect(websocket, user_id)

    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
```

### 3. Create Live Leaderboard

Real-time leaderboard updates:

```python
@router.websocket("/ws/leaderboard")
async def leaderboard_stream(websocket: WebSocket):
    """
    TODO: Live leaderboard stream
    - Broadcast leaderboard updates
    - Update when users complete missions
    - Show real-time rank changes
    """
    await websocket.accept()

    try:
        while True:
            # Send leaderboard every 5 seconds
            await asyncio.sleep(5)

            # Get current leaderboard
            users = db.query(User).order_by(
                User.experience_points.desc()
            ).limit(10).all()

            leaderboard = [{
                "rank": idx + 1,
                "username": user.username,
                "experience_points": user.experience_points
            } for idx, user in enumerate(users)]

            await websocket.send_json({
                "type": "leaderboard_update",
                "data": leaderboard,
                "timestamp": datetime.utcnow().isoformat()
            })

    except WebSocketDisconnect:
        pass
```

### 4. Implement Presence System

Track online/offline status:

```python
from datetime import datetime, timedelta

online_users = {}  # user_id -> last_seen


@router.get("/presence/online")
async def get_online_users():
    """
    TODO: Get list of online users
    - Check WebSocket connections
    - Check last activity time
    - Return list of online users
    """
    active_users = manager.get_active_users()
    return {
        "online_count": len(active_users),
        "users": active_users
    }


@router.websocket("/ws/presence/{user_id}")
async def presence_tracking(
    websocket: WebSocket,
    user_id: int
):
    """
    TODO: Track user presence
    - Send heartbeat every 30 seconds
    - Update last_seen timestamp
    - Notify others of status changes
    """
    await manager.connect(websocket, user_id)
    online_users[user_id] = datetime.utcnow()

    # Broadcast user is online
    await manager.broadcast({
        "type": "presence",
        "user_id": user_id,
        "status": "online"
    })

    try:
        while True:
            # Wait for heartbeat
            await websocket.receive_text()
            online_users[user_id] = datetime.utcnow()

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        if user_id in online_users:
            del online_users[user_id]

        # Broadcast user is offline
        await manager.broadcast({
            "type": "presence",
            "user_id": user_id,
            "status": "offline"
        })
```

### 5. Create Client-Side WebSocket Handler

Example HTML client (`static/websocket-test.html`):

```html
<!DOCTYPE html>
<html>
<head>
    <title>PyArena WebSocket Test</title>
</head>
<body>
    <h1>PyArena Live Chat</h1>

    <div id="status">Disconnected</div>
    <div id="messages" style="border: 1px solid #ccc; height: 300px; overflow-y: scroll;"></div>

    <input type="text" id="messageInput" placeholder="Type a message..." />
    <button onclick="sendMessage()">Send</button>

    <script>
        const userId = Math.floor(Math.random() * 1000); // TODO: Get from auth
        const ws = new WebSocket(`ws://localhost:8000/api/ws/${userId}`);

        ws.onopen = () => {
            document.getElementById('status').textContent = 'Connected';
            document.getElementById('status').style.color = 'green';
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const messagesDiv = document.getElementById('messages');

            let message = '';
            if (data.type === 'chat') {
                message = `User ${data.user_id}: ${data.message}`;
            } else if (data.type === 'user_joined') {
                message = `User ${data.user_id} joined`;
            } else if (data.type === 'user_left') {
                message = `User ${data.user_id} left`;
            }

            const p = document.createElement('p');
            p.textContent = `[${new Date(data.timestamp).toLocaleTimeString()}] ${message}`;
            messagesDiv.appendChild(p);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        };

        ws.onclose = () => {
            document.getElementById('status').textContent = 'Disconnected';
            document.getElementById('status').style.color = 'red';
        };

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value;

            if (message) {
                ws.send(JSON.stringify({
                    type: 'chat',
                    message: message
                }));
                input.value = '';
            }
        }

        // Send on Enter key
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
```

---

## 🧪 Testing Your Solution

```bash
# Start the server
poetry run uvicorn app.main:app --reload

# Open multiple browser tabs to:
open http://localhost:8000/static/websocket-test.html

# Or test with Python client
```

Python WebSocket client:

```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/api/ws/1"

    async with websockets.connect(uri) as websocket:
        # Receive welcome message
        response = await websocket.recv()
        print(f"< {response}")

        # Send a message
        await websocket.send(json.dumps({
            "type": "chat",
            "message": "Hello from Python!"
        }))

        # Listen for responses
        async for message in websocket:
            print(f"< {message}")

asyncio.run(test_websocket())
```

---

## 📖 Key Concepts

### WebSocket Lifecycle
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # 1. Accept connection
    try:
        while True:
            data = await websocket.receive_text()  # 2. Receive
            await websocket.send_text(f"Echo: {data}")  # 3. Send
    except WebSocketDisconnect:
        pass  # 4. Handle disconnect
```

---

## 🎓 Resources

- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [WebSocket Protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [JavaScript WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

---

## ✨ Completion Criteria

- [ ] Created WebSocket connection manager
- [ ] Implemented chat endpoint
- [ ] Built notification stream
- [ ] Created live leaderboard
- [ ] Implemented presence tracking
- [ ] Tested with multiple clients
- [ ] Created HTML test client
- [ ] Handled disconnections gracefully

---

## ⏭️ Next Mission

Real-time mastered! Progress to **Mission 12: The Mirror Gateway** to add GraphQL support.

*"The stream whispers secrets to those who listen..."*
