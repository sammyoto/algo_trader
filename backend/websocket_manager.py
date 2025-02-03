import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)

class WebSocket_Manager:
    def __init__(self):
        self.active_connections: Dict[tuple, Set[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, trader: str, ticker: str):
        key = (trader, ticker)
        async with self.lock:
            if key not in self.active_connections:
                self.active_connections[key] = set()
            self.active_connections[key].add(websocket)

    async def disconnect(self, websocket: WebSocket, trader: str, ticker: str):
        key = (trader, ticker)
        async with self.lock:
            if key in self.active_connections:
                self.active_connections[key].discard(websocket)
                if not self.active_connections[key]:
                    del self.active_connections[key]

    async def broadcast_to_subscribers(self, trader: str, ticker: str, message: dict):
        key = (trader, ticker)
        async with self.lock:
            connections = self.active_connections.get(key, set())
            for connection in connections.copy():  # Use copy to avoid size change during iteration
                try:
                    await connection.send_json(message)
                except WebSocketDisconnect:
                    await self.disconnect(connection, trader, ticker)