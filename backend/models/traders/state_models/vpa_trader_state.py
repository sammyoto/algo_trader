from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from typing import Optional, Annotated
from uuid import uuid4
from models.polygon_models import Timespan
from models.two_decimal import TwoDecimal, TwoDecimalType
from models.traders.state_models.trader_state import TraderState

class VPATraderState(TraderState, table=True):
    # Defaults
    type: str = Field(default="vpa")
    description: str = "A trader that trades using Volume Price Analysis."
    cash_basis: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    cash: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    profit: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    bought_price: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    current_price: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]

    # Specific to VPATrader
    ticker: str = Field(default="")
    timespan: Timespan = Field(default=Timespan.DAY)
    window: int = Field(default=3)
    volume_sensitivity: int = Field(default=20)
    selloff_percentage: int = Field(default=20)
    stoploss_percentage: int = Field(default=20)