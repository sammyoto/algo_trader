from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from services.trader_handler_service import TraderHandlerService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trader_handler_service = TraderHandlerService()

@app.on_event("startup")
async def startup_event():
    trader_handler_service.start_service()

@app.get("/")
async def root():
    return "Hello World!"

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8002, reload=True)