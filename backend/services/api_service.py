import json
from typing import List
from services.trader_handler_service import TraderHandlerService
from services.database_service import DatabaseService
from models.two_decimal import TwoDecimal
from models.traders.trader import Trader
from models.polygon_models import RestEndpoint, RestResponseKeys
from models.api_models import TraderCreationRequest, TraderType
from models.traders.simple_threshold_trader import SimpleThresholdTrader
from models.traders.vpa_trader import VPATrader
from models.traders.state_models.trader_state import TraderState

class ApiService:
    def __init__(self):
        self.db_service = DatabaseService()
        self.trader_handler_service = TraderHandlerService(db_service=self.db_service)

    def add_trader(self, trader_creation_request: TraderCreationRequest):
        if self.db_service.name_exists(trader_creation_request.name):
            raise ValueError(f"Trader with name '{trader_creation_request.name}' already exists, or has existed in the past. Please choose another name.")
        match trader_creation_request.trader_type:
            case TraderType.SIMPLE_THRESHOLD:
                trader = SimpleThresholdTrader(
                    state = TraderState(
                            name=trader_creation_request.name,
                            type="simple_threshold",
                            cash_basis=TwoDecimal(trader_creation_request.cash),
                            cash=TwoDecimal(trader_creation_request.cash),
                            paper=trader_creation_request.paper,
                            buy_threshold=TwoDecimal(trader_creation_request.buy_threshold),
                            sell_threshold=TwoDecimal(trader_creation_request.sell_threshold),
                            ticker=trader_creation_request.ticker
                    ),
                    db_service = self.db_service
                )                                        
            case TraderType.VOLUME_PRICE_ANALYSIS:
                trader = VPATrader(
                    state = TraderState(
                        name=trader_creation_request.name,
                        type="vpa",
                        cash_basis=TwoDecimal(trader_creation_request.cash),
                        cash=TwoDecimal(trader_creation_request.cash), 
                        paper=trader_creation_request.paper,
                        ticker=trader_creation_request.ticker, 
                        timespan=trader_creation_request.timespan, 
                        window=trader_creation_request.window, 
                        volume_sensitivity=trader_creation_request.volume_sensitivity, 
                        selloff_percentage=trader_creation_request.selloff_percentage, 
                        stoploss_percentage =trader_creation_request.stoploss_percentage,
                    ),
                    db_service = self.db_service 
                )
            case _:
                trader = SimpleThresholdTrader(
                    state = TraderState(
                        name="Default",
                        type="simple_threshold",
                        cash_basis=TwoDecimal(0),
                        cash=TwoDecimal(0),
                        buy_threshold=TwoDecimal(0),
                        sell_threshold=TwoDecimal(0),
                        ticker="NVDA"
                    ),
                    db_service = self.db_service
                )
        self.db_service.push_trader_state(trader.state)
        self.trader_handler_service.add_trader(trader, trader_creation_request.data_frequency)

    def delete_trader(self, trader_name: str):
        self.trader_handler_service.delete_trader(trader_name)

    def get_trader_by_name(self, trader_name: str) -> Trader|str:
        return self.trader_handler_service.get_trader(trader_name)

    def get_all_traders(self):
        print(self.trader_handler_service.get_trader_states())
        return self.trader_handler_service.get_trader_states()