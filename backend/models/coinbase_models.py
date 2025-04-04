from pydantic import BaseModel
from models.two_decimal import TwoDecimal

class MarketOrder(BaseModel):
    client_order_id: str
    product_id: str
    quote_size: str