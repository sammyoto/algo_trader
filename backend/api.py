from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from services.data_ingestion_service import DataIngestionService
from services.trader_handler_service import TraderHandlerService
from models.polygon_models import RestEndpoint, RestResponseKeys
from models.api_models import *
from polygon.rest.models import TickerSnapshot
import json

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

@app.on_event("startup")
async def startup_event():
    data_ingestion_service.start_service()
    trader_handler_service.start_service()

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/data/rest")
async def get_rest_endpoint(endpoint: RestEndpoint):
    try:
        response = data_ingestion_service.pr.get_endpoint(endpoint)
        return APIResponse(status=Status.SUCCESS,  message="Response returned succesfully.", body=response)
    except:
        return APIResponse(status=Status.FAILED, message="Response failed.", body=None)
    

@app.post("/data/rest")
async def subscribe_to_rest_endpoint(endpoint: RestEndpoint):
    try:
        data_ingestion_service.pr.subscribe_to_endpoint(endpoint)
        return APIResponse(status=Status.SUCCESS, message="Subscribed to endpoint successfully.", body=None)
    except:
        return APIResponse(status=Status.FAILED, message="Subscribe failed.", body=None)
    
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)