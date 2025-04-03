from shared_services.redis_service import RedisService
from typing import Union, Optional, List, Dict
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from models.traders.trader import Trader
from models.api_models import DataFrequency

class TraderHandlerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.traders : Dict[str, Trader] = {}

    def add_trader(self, trader: Trader, data_frequency: DataFrequency):
        trader.set_message_callback(self.print_trader_message)
        self.traders[trader.name] = trader
        self.scheduler.add_job(
            trader.step,
            IntervalTrigger(
                days=data_frequency.days,
                hours=data_frequency.hours,
                minutes=data_frequency.minutes,
                seconds=data_frequency.seconds
            ),
            id=trader.name
        )

    def print_trader_message(self, message):
        print(message)

    def delete_trader(self, trader_name: str):
        del self.traders[trader_name]
    
    def get_traders(self):
        return self.traders