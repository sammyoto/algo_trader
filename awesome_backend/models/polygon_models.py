from pydantic import BaseModel
from typing import Union, Optional
import json
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
    params: dict
    redis_channel: str

    def __init__(self, event: RestEvents, params: BaseModel):
        super().__init__(event=event, params=params.model_dump(), redis_channel="")
        self.redis_channel = self.get_channel_name()

    def serialize_param(self, param):
        if isinstance(param, dict):
            return json.dumps(param, separators=(',', ':'))
        elif isinstance(param, list):
            return json.dumps(param, separators=(',', ':'))
        elif isinstance(param, Enum):
            return param.value
        else:
            return str(param)

    def get_channel_name(self):
        name = self.event.value
        
        serialized_params = [
            f"({key}, {self.serialize_param(value)})"
            for key, value in self.params.items()
        ]
        return f"{name}." + '.'.join(serialized_params)

class WebSocketEndpoint(BaseModel):
    event: WebSocketEvents
    ticker: str

class SimpleMovingAverageRestEndpoint(BaseModel):
    ticker: str
    series_type: SeriesTypes
    timespan: str
    window: int