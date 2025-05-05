from shared_services.redis_service import RedisService
from typing import Union, Optional, List, Dict
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from models.traders.trader import Trader
from models.api_models import DataFrequency
from services.database_service import DatabaseService

class TraderHandlerService:
    def __init__(self, db_service: DatabaseService):
        self.scheduler = BackgroundScheduler()
        self.db_service = db_service
        self.traders : Dict[str, Trader] = {}

    def add_trader(self, trader: Trader, data_frequency: DataFrequency):
        trader.set_message_callback(self.print_trader_message)
        self.traders[trader.state.name] = trader
        self.scheduler.add_job(
            trader.step,
            IntervalTrigger(
                days=data_frequency.days,
                hours=data_frequency.hours,
                minutes=data_frequency.minutes,
                seconds=data_frequency.seconds
            ),
            id=trader.state.name
        )

    def print_trader_message(self, message):
        print(message)

    def delete_trader(self, trader_name: str):
        self.scheduler.remove_job(trader_name)
        del self.traders[trader_name]
    
    def get_traders(self):
        return self.traders