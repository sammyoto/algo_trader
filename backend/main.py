from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from data_streamer import Data_Streamer
from websocket_manager import WebSocket_Manager
from helper_functions import valid_trader_ticker
from starlette.middleware.base import BaseHTTPMiddleware

app_key = "GAoJ8adVvh8wkIOpGe6zIIAgVmpw6ZnK"
secret_key = "BoEhNQ1GcrMT8X4A"
tickers = ["NVDA", "AMZN", "GOOG", "BAH"]

# for allowing websocket connection to localhost
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "connect-src 'self' ws://localhost:8000 wss://localhost:8000; "
            "default-src 'self';"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

app = FastAPI(middleware=[
    Middleware(SecurityHeadersMiddleware)
])
websocket_manager = WebSocket_Manager()
streamer = Data_Streamer(app_key, secret_key, tickers, websocket_manager)

@app.on_event("startup")
async def startup_event():
    await websocket_manager.start()
    streamer.start()

@app.on_event("shutdown")
async def shutdown_event():
    streamer.stop()
    await websocket_manager.stop()
    await websocket_manager.broadcast_system_message("Server shutting down")

@app.get("/")
async def root():
    result = streamer.get_data()
    return result

@app.websocket("/ws/{trader}/{ticker}")
async def websocket_endpoint(websocket: WebSocket, trader: str, ticker: str):
    # Validate trader/ticker combination
    if not valid_trader_ticker(trader, ticker):
        await websocket.close()
        return

    await websocket_manager.connect(websocket, trader, ticker)
    try:
        while True:
            # Handle incoming messages (e.g., unsubscribe requests)
            data = await websocket.receive_text()
            if data == "unsubscribe":
                break
    except WebSocketDisconnect:
        pass
    finally:
        await websocket_manager.disconnect(websocket, trader, ticker)