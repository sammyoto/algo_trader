from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from services.data_ingestion_service import DataIngestionService
from services.trader_handler_service import TraderHandlerService
from services.api_service import ApiService
from models.polygon_models import RestEndpoint, RestResponseKeys, WebSocketEndpoint
from models.api_models import *
from models.trader import Trader
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

data_ingestion_service = DataIngestionService()
trader_handler_service = TraderHandlerService()
api_service = ApiService(data_ingestion_service, trader_handler_service)

@app.on_event("startup")
async def startup_event():
    data_ingestion_service.start_service()

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/data/rest")
async def get_rest_endpoint(endpoint: RestEndpoint):
    try:
        response = api_service.get_rest_endpoint(endpoint)
        return APIResponse(status=Status.SUCCESS,  message="Response returned succesfully.", body=response)
    except Exception as e:
        return APIResponse(status=Status.FAILED, message="Response failed.", body=str(e))

@app.post("/data/rest")
async def subscribe_to_rest_endpoint(endpoint: RestEndpoint):
    try:
        api_service.subscribe_to_rest_endpoint(endpoint)
        return APIResponse(status=Status.SUCCESS, message="Subscribed to endpoint successfully.", body=None)
    except Exception as e:
        return APIResponse(status=Status.FAILED, message="Subscribe failed.", body=str(e))
    
@app.delete("/data/rest")
async def delete_rest_endpoint(endpoint: RestEndpoint):
    try:
        api_service.delete_rest_endpoint(endpoint)
        return APIResponse(status=Status.SUCCESS, message="Endpoint deleted successfully.", body=None)
    except Exception as e:
        return APIResponse(status=Status.FAILED, message="Endpoint deletion failed.", body=str(e))
    
@app.post("/data/ws")
async def subscribe_to_websocket_endpoint(endpoint: WebSocketEndpoint):
    try:
        api_service.subscribe_to_ws_endpoint(endpoint)
        return APIResponse(status=Status.SUCCESS, message="Subscribed to endpoint successfully.", body=None)
    except Exception as e:
        return APIResponse(status=Status.FAILED, message="Subscribe failed.", body=str(e))
    
@app.post("/trader")
async def add_trader(trader: Trader):
    try:
        api_service.add_trader(trader)
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