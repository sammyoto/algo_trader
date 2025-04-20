from fastapi import FastAPI
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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


trader_handler_service = TraderHandlerService()
api_service = ApiService(trader_handler_service)

@app.get("/")
async def root():
    return "Hello World!"
    
@app.post("/trader")
async def add_trader(trader_creation_request: TraderCreationRequest):
    try:
        api_service.add_trader(trader_creation_request)
        return APIResponse(status=Status.SUCCESS, message="Added trader successfully.", body=None)
    except Exception as e:
        return APIResponse(status=Status.FAILED, message="Add trader failed.", body=str(e))
    
@app.get("/trader")
async def get_all_traders():
    try:
        traders = api_service.get_all_traders()
        return APIResponse(status=Status.SUCCESS, message="Get traders succeeded.", body=traders)
    except Exception as e:
        return APIResponse(status=Status.FAILED, message="Get traders failed.", body=str(e))
    
@app.delete("/trader")
async def delete_trader(trader_name: str):
    try:
        api_service.delete_trader(trader_name)
        return APIResponse(status=Status.SUCCESS, message="Trader deleted", body=None)
    except Exception as e:
        return APIResponse(status=Status.FAILED, message="Trader deletion failed.", body=str(e))
    
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)