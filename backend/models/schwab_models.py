from pydantic import BaseModel
from models.two_decimal import TwoDecimal
from typing import Union, Optional, List, Dict

class BasicOrder(BaseModel):
    orderType: str = "LIMIT"
    session: str = "NORMAL"
    duration: str = "DAY"
    orderStrategyType: str = "SINGLE"
    price: TwoDecimal
    orderLegCollection: List[Dict]

    def __init__(self, price: TwoDecimal, instruction: str, quantity: int, symbol: str):
        order = [{
            "instruction": instruction,
            "quantity": quantity,
            "instrument": {
                "symbol": symbol,
                "assetType": "EQUITY"
            }
        }]
        super.__init__(price = price, orderLegCollection = order)