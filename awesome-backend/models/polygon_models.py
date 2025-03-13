from pydantic import BaseModel
from typing import Union, Optional
from enum import Enum

class RestEndpoint(BaseModel):
    function: str
    ticker: str

class WebSocketEvents(str, Enum):
    AGG_MIN = "AM"
    AGG_SEC = "A"
    TRADES = "T"
    QUOTES = "Q"

class WebSocketEndpoint(BaseModel):
    event: WebSocketEvents
    ticker: str