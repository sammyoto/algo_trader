from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from typing import Optional
from uuid import uuid4
from models.two_decimal import TwoDecimal, TwoDecimalType

class TraderState(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    type: str = "base"
    name: str
    description: str = "Trader Base Model."
    cash_basis: TwoDecimal = Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))
    cash: TwoDecimal = Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))
    profit: TwoDecimal = Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))
    bought_price: TwoDecimal = Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))
    current_price: TwoDecimal = Field(default=TwoDecimal(0), sa_column=Column(TwoDecimalType))
    holdings: int = 0
    holding: bool = False
    awaiting_trade_confirmation: bool = False
    order_id: Optional[str]
    paper: bool

    __mapper_args__ = {
        "polymorphic_on": "type",         # which column tells us the subclass
        "polymorphic_identity": "base"    # what value means "this is a base trader"
    }