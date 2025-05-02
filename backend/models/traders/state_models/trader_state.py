from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from typing import Optional
from uuid import uuid4
from models.two_decimal import TwoDecimal, TwoDecimalType

class TraderState(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    description: str
    cash_basis: TwoDecimal = Field(sa_column=Column(TwoDecimalType))
    cash: TwoDecimal = Field(sa_column=Column(TwoDecimalType))
    profit: TwoDecimal = Field(sa_column=Column(TwoDecimalType))
    bought_price: TwoDecimal = Field(sa_column=Column(TwoDecimalType))
    current_price: TwoDecimal = Field(sa_column=Column(TwoDecimalType))
    holdings: int
    holding: bool
    awaiting_trade_confirmation: bool
    order_id: Optional[str]
    paper: bool
    trader_type: str  # helps you reload correct logic class