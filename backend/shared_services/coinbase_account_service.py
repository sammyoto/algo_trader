from models.coinbase_models import MarketOrder
from coinbase.rest import RESTClient
from json import dumps

class CoinbaseAccountService:
    def __init__(self, api_key: str, api_secret: str, debug: bool = True):
        self.debug = debug
        self.client = RESTClient(
            api_key = api_key,
            api_secret = api_secret
        )

    def get_account(self):
        accounts = self.client.get_accounts()
        print(dumps(accounts.to_dict(), indent=2))

    def execute_trade(self, order: MarketOrder):
        if self.debug:
            return "Filled"
        else:
            self.client.market_order_buy(**order)
        
    def get_order_status(self, order_id: str):
        return "Filled"