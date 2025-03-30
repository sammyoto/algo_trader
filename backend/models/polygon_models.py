from pydantic import BaseModel
from typing import Union, Optional
from polygon.rest.models import TickerSnapshot, SMAIndicatorResults, LastQuote
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

class RestResponseKeys:
    mapping = {
        RestEvents.GET_SNAPSHOT_TICKER: "ticker",
        RestEvents.GET_SIMPLE_MOVING_AVERAGE: "results",
        RestEvents.GET_LAST_QUOTE: "results",
    }

    @classmethod
    def get_key(cls, event: RestEvents) -> str:
        return cls.mapping.get(event)
    
class RestResponseType:
    mapping = {
        RestEvents.GET_SNAPSHOT_TICKER: TickerSnapshot,
        RestEvents.GET_SIMPLE_MOVING_AVERAGE: SMAIndicatorResults,
        RestEvents.GET_LAST_QUOTE: LastQuote,
    }

    @classmethod
    def get_type(cls, function: str):
        return cls.mapping.get(function)

class WebSocketEvents(str, Enum):
    AGG_MIN = "AM"
    AGG_SEC = "A"
    TRADES = "T"
    QUOTES = "Q"

class RestEndpoint(BaseModel):
    event: RestEvents
    params: dict
    redis_channel: str

    def __init__(self, event: RestEvents, params: dict):
        super().__init__(event=event, params=params, redis_channel="")
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
    endpoint_str: str

    def __init__(self, event: WebSocketEvents, ticker: str):
        super().__init__(event=event, ticker=ticker, endpoint_str = "")
        self.endpoint_str = f"{event}.{ticker}"