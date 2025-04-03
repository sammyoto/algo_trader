from pydantic import BaseModel
from typing import Generic, TypeVar, Union, Optional, List, Literal
from enum import Enum

T = TypeVar("T")

class Status(int, Enum):
    FAILED = 400
    SUCCESS = 200

class APIResponse(BaseModel, Generic[T]):
    status: Status
    message: str
    body: Optional[T]

class DataFrequency(BaseModel):
    days: int
    hours: int
    minutes: int
    seconds: int
    
    def convert_to_seconds(self):
        return (
            self.days * 86400 +
            self.hours * 3600 +
            self.minutes * 60 + 
            self.seconds
        )
    
class TraderType(str, Enum):
    SIMPLE_THRESHOLD = "simple_threshold"
    
class BaseTraderCreationRequest(BaseModel):
    trader_type: TraderType
    name: str
    data_frequency: DataFrequency

class SimpleThresholdTraderCreationRequest(BaseTraderCreationRequest):
    trader_type: Literal[TraderType.SIMPLE_THRESHOLD]
    buy_threshold: float
    sell_threshold: float
    ticker: str

TraderCreationRequest = Union[
                                SimpleThresholdTraderCreationRequest
                            ]