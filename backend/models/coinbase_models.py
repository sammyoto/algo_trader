from pydantic import BaseModel
from models.two_decimal import TwoDecimal

class MarketOrder(BaseModel):
    client_order_id: str
    product_id: str
    quote_size: str

class PortfolioStats(BaseModel):
    total_balance: float
    cash_balance: float
    crypto_balance: float