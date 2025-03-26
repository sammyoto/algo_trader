from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.data_ingestion_service import DataIngestionService
from shared.models.polygon_models import RestEndpoint
from shared.models.api_models import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_ingestion_service = DataIngestionService()

@app.on_event("startup")
async def startup_event():
    data_ingestion_service.start_service()

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/rest")
async def get_rest_endpoint(endpoint: RestEndpoint):
    try:
        response = data_ingestion_service.pr.get_endpoint(endpoint)
        return APIResponse(Status.SUCCESS,  "Response returned succesfully.", response)
    except:
        return APIResponse(Status.FAILED, "Response failed.", None)
    

@app.post("/rest")
async def subscribe_to_rest_endpoint(endpoint: RestEndpoint):
    try:
        data_ingestion_service.pr.subscribe_to_endpoint(endpoint)
        return APIResponse(Status.SUCCESS, "Subscribed to endpount successfully.", None)
    except:
        return APIResponse(Status.FAILED, "Subscribe failed.", None)
