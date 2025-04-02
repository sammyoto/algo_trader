from shared_services.redis_service import RedisService
from typing import Union, Optional, List, Dict
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from backend.models.traders.trader import Trader

class TraderHandlerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.traders : Dict[str, Trader] = {}

    def add_trader(self, trader: Trader):
        self.traders[trader.name] = trader
        self.scheduler.add_job(
            trader.step,
            IntervalTrigger(seconds=5),
            id=trader.name
        )

    def delete_trader(self, trader_name: str):
        del self.traders[trader_name]
    
    def get_traders(self):
        return self.traders