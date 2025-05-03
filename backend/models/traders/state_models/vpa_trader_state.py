from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from typing import Optional
from uuid import uuid4
from models.polygon_models import Timespan
from models.two_decimal import TwoDecimal, TwoDecimalType
from models.traders.state_models.trader_state import TraderState

class VPATraderState(TraderState, table=False):
    ticker: str
    timespan: Timespan
    window: int
    volume_sensitivity: int
    selloff_percentage: int
    stoploss_percentage: int

    __mapper_args__ = {
        "polymorphic_identity": "vpa"
    }