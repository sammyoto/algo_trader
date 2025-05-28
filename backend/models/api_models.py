from pydantic import BaseModel
from typing import Generic, TypeVar, Union, Optional, List, Literal
from models.polygon_models import Timespan
from enum import Enum
from models.trader_models import TraderType

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
    
class TraderCreationRequest(BaseModel):
    trader_type: TraderType
    name: str
    cash: str
    paper: bool = True
    init_data: Optional[dict] = None
    data_frequency: DataFrequency
    ticker: Optional[str] = None
    buy_threshold: Optional[str] = None
    sell_threshold: Optional[str] = None
    timespan: Optional[Timespan] = None
    window: Optional[int] = None
    volume_sensitivity: Optional[int] = None
    selloff_percentage: Optional[int] = None
    stoploss_percentage: Optional[int] = None