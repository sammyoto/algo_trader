from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import Column, DateTime
from typing import Optional, Annotated
from models.polygon_models import Timespan
from uuid import uuid4
from models.two_decimal import TwoDecimal, TwoDecimalType

class TraderState(SQLModel, table=True):
    __tablename__ = "trader_state"
    # Default for every trader
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),  sa_column=Column(DateTime, default=datetime.now(timezone.utc)))
    type: str = Field(default="base")
    name: str = Field(index=True)
    cash_basis: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    cash: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    profit: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    bought_price: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    current_price: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))]
    holdings: int = Field(default=0)
    holding: bool = Field(default=False)
    awaiting_trade_confirmation: bool = Field(default=False)
    order_id: Optional[str] = Field(default=None, nullable=True)
    paper: bool = Field()

    # Shared
    ticker: Optional[str] = Field(default="")
    # SimpleThreshold Trader
    buy_threshold: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))] = None
    sell_threshold: Annotated[TwoDecimal, Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))] = None
    # VPA Trader
    timespan: Optional[Timespan] = Field(default=Timespan.DAY)
    window: Optional[int] = Field(default=3)
    volume_sensitivity: Optional[int] = Field(default=20)
    selloff_percentage: Optional[int] = Field(default=20)
    stoploss_percentage: Optional[int] = Field(default=20)