from sqlmodel import SQLModel, Field
from typing import Any
from sqlalchemy import Column
from typing import Optional, Annotated
from uuid import uuid4
from models.two_decimal import TwoDecimal, TwoDecimalType
from models.traders.state_models.trader_state import TraderState

class SimpleThresholdTraderState(TraderState, table=True):
    # Defaults, necessary to map TWoDecimal to SQLAlchemy
    type: str = Field(default="simple_threshold")
    description: str = Field(default="A trader that buys and sells at specific price points.")
    cash_basis: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    cash: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    profit: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    bought_price: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    current_price: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]

    # Specific to SimpleThresholdTrader
    buy_threshold: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))] = None
    sell_threshold: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))] = None
    ticker: str = Field(default="")