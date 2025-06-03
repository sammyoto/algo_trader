from pydantic import BaseModel, PrivateAttr
from typing import Union, Optional, List, Dict
from shared_services.redis_service import RedisService
from shared_services.polygon_rest_service import PolygonRESTService
from shared_services.schwab_account_service import SchwabAccountService
from shared_services.coinbase_account_service import CoinbaseAccountService
from models.polygon_models import RestEndpoint, RestResponseType, RestEvents
from models.redis_models import RedisMessage
from models.two_decimal import TwoDecimal
from models.traders.state_models.trader_state import TraderState
from models.schwab_models import BasicOrder
from services.database_service import DatabaseService
import os

class Trader(BaseModel):
    state: TraderState

    _d: DatabaseService = PrivateAttr()
    _r: RedisService = PrivateAttr()
    _p: PolygonRESTService = PrivateAttr()
    _a: SchwabAccountService = PrivateAttr()
    _current_order: BasicOrder|None = PrivateAttr()
    _message_callback: callable = PrivateAttr()

    def __init__(self, state: TraderState, schwab_account: SchwabAccountService, coinbase_account: CoinbaseAccountService, db_service: DatabaseService = None, init_data = None):
        super().__init__(state = state)
        self._d = db_service
        self._p = PolygonRESTService(
            os.getenv("POLYGON_API_KEY")
        )
        self._a = schwab_account
        self._c = coinbase_account
        self._current_order = None

        # function used to initialize trader values if needed
        if init_data is not None:
            self.on_trader_init(data=init_data)
        else:
            self.on_trader_init(self.get_init_data())

    def update_trader_after_trade(self):
        pass

    def verify_order_execution(self):
        if self._a.get_order_status(self.state.order_id) == "Filled":
            self.state.awaiting_trade_confirmation = False
            self.state.order_id = None
            self.update_trader_after_trade()

            return "Filled"
        
        return "Waiting"
    
    def bsh(self):
        pass
    
    def update_trader(self, data):
        pass
    
    def get_data(self):
        pass

    def get_init_data(self):
        pass

    def on_trader_init(self, data):
        pass

    def set_paper(self, paper: bool):
        self.reset_trader()
        self.state.paper = paper
        self._a.set_paper(paper)

    def reset_trader(self):
        self.state.cash = self.state.cash_basis
        self.state.awaiting_trade_confirmation = False
        self.state.order_id = None
        self.state.profit = TwoDecimal(0)
        self.state.bought_price = TwoDecimal(0)
        self.state.current_price = TwoDecimal(0)
        self.state.holdings = 0
        self.state.holding = False
        self._current_order = None

    def get_trader_data(self):
        return self.model_dump()

    def set_message_callback(self, callback: callable):
        self._callback = callback

    def step(self, data=None):
        if self.state.awaiting_trade_confirmation:
            status = self.verify_order_execution()
            if status == "Waiting":
                return
            
        if data is None:
            data = self.get_data()

        self.update_trader(data)
        self.bsh()

        if self._d != None:
            self._d.push_trader_state(self.state)