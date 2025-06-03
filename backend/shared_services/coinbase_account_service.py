from models.coinbase_models import MarketOrder, PortfolioStats
from coinbase.rest import RESTClient
from json import dumps

class CoinbaseAccountService:
    def __init__(self, api_key: str, api_secret: str):
        self.client = RESTClient(
            api_key = api_key,
            api_secret = api_secret
        )
    
    def get_portoflio_stats(self):
        portfolio = self.client.get_portfolio_breakdown(portfolio_uuid="5127c702-c631-58f2-a3e8-1a35f9af78fc").to_dict()
        portoflio_stats: PortfolioStats = {
            "total_balance": portfolio["breakdown"]["portfolio_balances"]["total_balance"]["value"],
            "cash_balance": portfolio["breakdown"]["portfolio_balances"]["total_cash_equivalent_balance"]["value"],
            "crypto_balance": portfolio["breakdown"]["portfolio_balances"]["total_crypto_balance"]["value"]
        }
        return portoflio_stats

    def execute_trade(self, order: MarketOrder, paper: bool):
        if paper:
            return "Filled"
        else:
            self.client.market_order_buy(**order)
        
    def get_order_status(self, order_id: str):
        return "Filled"