from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from typing import Optional, Any, Annotated
from uuid import uuid4
from models.two_decimal import TwoDecimal, TwoDecimalType
from models.polygon_models import Timespan
from datetime import datetime, timezone

class TraderState(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    type: str = Field(default="base")
    name: str = Field(index=True)
    description: str = Field(default="Trader Base Model.")
    cash_basis: TwoDecimal = Field(default=TwoDecimal(0))
    cash: TwoDecimal = Field(default=TwoDecimal(0))
    profit: TwoDecimal = Field(default=TwoDecimal(0))
    bought_price: TwoDecimal = Field(default=TwoDecimal(0))
    current_price: TwoDecimal = Field(default=TwoDecimal(0))
    holdings: int = Field(default=0)
    holding: bool = Field(default=False)
    awaiting_trade_confirmation: bool = Field(default=False)
    order_id: Optional[str] = Field(default=None, nullable=True)
    paper: bool = Field()
    #timestamp: datetime = Field(default=datetime.now(timezone.utc), index=True)