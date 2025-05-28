from pydantic import BaseModel
from typing import Union, Optional, List
from polygon.rest.models import TickerSnapshot, SMAIndicatorResults, LastQuote, DailyOpenCloseAgg
from datetime import datetime
import json
from enum import Enum

class SimpleThresholdDataSchema(BaseModel):
    quote: LastQuote

class VPADataSchema(BaseModel):
    sma: SMAIndicatorResults
    dailyAggs: DailyOpenCloseAgg
    quote: LastQuote

class VPAInitializationDataSchema(BaseModel):
    sma: SMAIndicatorResults
    dailyAggs: List[DailyOpenCloseAgg]

class TraderStatus(str, Enum):
    ACTIVE = "active"
    RETIRED = "retired"