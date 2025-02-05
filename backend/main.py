from fastapi import FastAPI, WebSocket,  WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from data_streamer import Data_Streamer
from websocket_manager import WebSocket_Manager
from helper_functions import valid_trader_ticker

app_key = "GAoJ8adVvh8wkIOpGe6zIIAgVmpw6ZnK"
secret_key = "BoEhNQ1GcrMT8X4A"
tickers = ["NVDA", "AMZN", "GOOG", "BAH"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

websocket_manager = WebSocket_Manager()
streamer = Data_Streamer(app_key, secret_key, tickers, websocket_manager)

@app.on_event("startup")
async def startup_event():
    streamer.start()

@app.on_event("shutdown")
async def shutdown_event():
    streamer.stop()

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/account_data")
async def account_data():
    return streamer.get_account_data()

@app.websocket("/ws/{trader}/{ticker}")
async def websocket_endpoint(websocket: WebSocket, trader: str, ticker: str):
    await websocket.accept()
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