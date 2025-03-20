from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.data_ingestion_service import DataIngestionService
from services.trader_handler_service import TraderHandlerService

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

@app.on_event("startup")
async def startup_event():
    data_ingestion_service.start_service()
    trader_handler_service.start_service()

@app.get("/")
async def root():
    return "Hello World!"
 
@app.post("/trader")
async def create_trader(trader_info):
    pass