from shared_services.redis_service import RedisService
from typing import Union, Optional, List, Dict
from models.trader import Trader

class TraderHandlerService:
    def __init__(self):
        self.traders : Dict[str, Trader] = {}

    def add_trader(self, trader: Trader):
        self.traders[trader.name] = trader
        trader.start()

    def delete_trader(self, trader_name: str):
        del self.traders[trader_name]
        print(self.traders)
    
    def get_traders(self):
        return self.traders