from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.data_ingestion_service import DataIngestionService

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