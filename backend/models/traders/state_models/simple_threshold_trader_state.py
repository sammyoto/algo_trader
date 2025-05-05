from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from typing import Optional
from uuid import uuid4
from models.two_decimal import TwoDecimal, TwoDecimalType
from models.traders.state_models.trader_state import TraderState

class SimpleThresholdTraderState(TraderState, table=False):
    type: str = "simple_threshold"
    buy_threshold: TwoDecimal = Field(sa_column=Column(TwoDecimalType))
    sell_threshold: TwoDecimal = Field(sa_column=Column(TwoDecimalType))
    ticker: str

    __mapper_args__ = {
        "polymorphic_identity": "simple_threshold"
    }