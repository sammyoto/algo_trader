from pydantic import BaseModel
from models.two_decimal import TwoDecimal
from typing import Union, Optional, List, Dict

class Instrument(BaseModel):
    symbol: str
    assetType: str = "EQUITY"

class OrderLegCollection(BaseModel):
    instruction: str
    quantity: int
    instrument: Instrument

class BasicOrder(BaseModel):
    orderType: str = "LIMIT"
    session: str = "NORMAL"
    duration: str = "DAY"
    orderStrategyType: str = "SINGLE"
    price: TwoDecimal
    orderLegCollection: List[OrderLegCollection]

    def __init__(self, price: TwoDecimal, instruction: str, quantity: int, symbol: str):
        order_leg_collection = OrderLegCollection(instruction=instruction, quantity=quantity, instrument=Instrument(symbol=symbol))
        order = [order_leg_collection]
        super().__init__(price = price, orderLegCollection = order)

    def get_price(self):
        return self.price

    def get_instruction(self):
        return self.orderLegCollection[0].instruction
    
    def get_quantity(self):
        return self.orderLegCollection[0].quantity
    
    def get_symbol(self):
        return self.orderLegCollection[0].instrument.symbol