from pydantic import BaseModel
from typing import Union, Optional, List
from enum import Enum

class TraderAlgorithms(str, Enum):
    PIVOT = "pivot"

class APIResponse(BaseModel):
    status: str
    message: str

class TraderCreationRequest(BaseModel):
    type: TraderAlgorithms
    tickers: Optional[List[str]]