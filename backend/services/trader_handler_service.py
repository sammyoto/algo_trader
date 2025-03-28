from shared_services.redis_service import RedisService
from typing import Union, Optional, List, Dict
from models.trader import Trader

class TraderHandlerService:
    def __init__(self):
        self.traders : Dict[str, Trader] = {}

    def add_trader(self, trader: Trader):
        self.traders[trader.name] = trader
        trader.start()