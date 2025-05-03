import json
from typing import List
from services.trader_handler_service import TraderHandlerService
from services.database_service import DatabaseService
from models.traders.trader import Trader
from models.polygon_models import RestEndpoint, RestResponseKeys
from models.api_models import TraderCreationRequest, TraderType
from models.traders.simple_threshold_trader import SimpleThresholdTrader
from models.traders.vpa_trader import VPATrader

class ApiService:
    def __init__(self):
        self.trader_handler_service = TraderHandlerService()
        self.db_service = DatabaseService()

    def add_trader(self, trader_creation_request: TraderCreationRequest):
        match trader_creation_request.trader_type:
            case TraderType.SIMPLE_THRESHOLD:
                trader = SimpleThresholdTrader(
                    name=trader_creation_request.name,
                    cash=trader_creation_request.cash,
                    paper=trader_creation_request.paper,
                    buy_threshold=trader_creation_request.buy_threshold,
                    sell_threshold=trader_creation_request.sell_threshold,
                    ticker=trader_creation_request.ticker
                )
            case TraderType.VOLUME_PRICE_ANALYSIS:
                trader = VPATrader(
                    name=trader_creation_request.name, 
                    cash=trader_creation_request.cash, 
                    paper=trader_creation_request.paper,
                    ticker=trader_creation_request.ticker, 
                    timespan=trader_creation_request.timespan, 
                    window=trader_creation_request.window, 
                    volume_sensitivity=trader_creation_request.volume_sensitivity, 
                    selloff_percentage=trader_creation_request.selloff_percentage, 
                    stoploss_percentage =trader_creation_request.stoploss_percentage,
                )
            case _:
                trader = SimpleThresholdTrader(
                    name="Default",
                    cash=0.0,
                    buy_threshold=0,
                    sell_threshold=0,
                    ticker="NVDA"
                )

        self.trader_handler_service.add_trader(trader, trader_creation_request.data_frequency)

    def delete_trader(self, trader_name: str):
        self.trader_handler_service.delete_trader(trader_name)

    def get_all_traders(self):
        return self.trader_handler_service.get_traders()
    
    def get_trader_by_name(self, trader_name: str):
        if trader_name in self.trader_handler_service.traders.keys():
            return self.trader_handler_service.traders[trader_name]
        
        return "Trader not found."