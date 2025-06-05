from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from services.trader_handler_service import TraderHandlerService
from services.api_service import ApiService
from models.polygon_models import RestEndpoint, RestResponseKeys
from models.api_models import *
from models.traders.trader import Trader
from polygon.rest.models import TickerSnapshot
import json

load_dotenv()

api_service = ApiService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic here (optional)
    yield
    print("Shutting down...")
    api_service.retire_all_traders()
    print("Shut down!")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "Hello World!"

# TRADER ENDPOINTS
@app.post("/trader")
async def add_trader(trader_creation_request: TraderCreationRequest):
    try:
        api_service.add_trader(trader_creation_request)
        return "Added trader successfully."
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Create trader failed: {str(e)}"
        )
    
@app.get("/trader")
async def get_all_traders():
    try:
        traders = api_service.get_latest_traders()
        return traders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Get all trader failed: {str(e)}"
        )
    
@app.get("/trader/{trader_name}")
async def get_trader_by_name(trader_name: str):
    try:
        trader = api_service.get_trader_by_name(trader_name)
        if trader == "Trader not found.":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=trader)
        return trader
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Get trader by name failed: {str(e)}"
        )
    
@app.get("/trader/live_switch/{trader_name}")
async def trader_live_switch(trader_name: str):
    try:
        api_service.trader_live_switch(trader_name)
        return "Trader is live."
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Trader live switch failed: {str(e)}"
        )
    
@app.delete("/trader/{trader_name}")
async def retire_trader(trader_name: str):
    try:
        api_service.retire_trader(trader_name)
        return "Trader retired."
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Get crypto account failed: {str(e)}"
        )
    
# ACCOUNT ENDPOINTS
@app.get("/account/crypto")
async def get_crypto_portfolio_stats():
    try:
        account = api_service.get_crypto_portfolio_stats()
        return account
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Get crypto account failed: {str(e)}"
        )
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)