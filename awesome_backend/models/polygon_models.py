from pydantic import BaseModel
from typing import Union, Optional
from enum import Enum

class MarketTypes(str, Enum):
    STOCKS = "stocks"

class SeriesTypes(str, Enum):
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"

class RestEvents(str, Enum):
    GET_SNAPSHOT_TICKER = "get_snapshot_ticker"
    GET_SIMPLE_MOVING_AVERAGE = "get_sma"
    GET_LAST_QUOTE = "get_last_quote"

class WebSocketEvents(str, Enum):
    AGG_MIN = "AM"
    AGG_SEC = "A"
    TRADES = "T"
    QUOTES = "Q"

class RestEndpoint(BaseModel):
    event: RestEvents
    params: BaseModel

class WebSocketEndpoint(BaseModel):
    event: WebSocketEvents
    ticker: str

class SimpleMovingAverageRestEndpoint(BaseModel):
    ticker: str
    series_type: SeriesTypes
    timespan: str
    window: int