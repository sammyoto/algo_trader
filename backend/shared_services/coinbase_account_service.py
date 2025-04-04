from models.coinbase_models import MarketOrder
from coinbase.rest import RESTClient

class CoinbaseAccountService:
    def __init__(self, debug: bool, api_key: str, api_secret: str):
        self.debug = debug
        self.client = RESTClient(
            api_key = api_key,
            api_secret = api_secret
        )

    def execute_trade(self, order: MarketOrder):
        if self.debug:
            return "Filled"
        else:
            self.client.market_order_buy(**order)
        
    def get_order_status(self, order_id: str):
        return "Filled"