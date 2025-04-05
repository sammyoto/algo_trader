from pydantic import BaseModel, PrivateAttr
from typing import Union, Optional, List, Dict
from shared_services.redis_service import RedisService
from shared_services.polygon_rest_service import PolygonRESTService
from shared_services.schwab_account_service import SchwabAccountService
from models.polygon_models import RestEndpoint, RestResponseType, RestEvents
from models.redis_models import RedisMessage
from models.two_decimal import TwoDecimal
from models.schwab_models import BasicOrder
import os

class Trader(BaseModel):
    name: str
    cash: TwoDecimal
    description: str = "Default Trader."
    awaiting_trade_confirmation: bool = False
    order_id: str | None = None
    current_order: BasicOrder | None = None

    _r: RedisService = PrivateAttr()
    _p: PolygonRESTService = PrivateAttr()
    _a: SchwabAccountService = PrivateAttr()
    _message_callback: callable = PrivateAttr()

    # **args is necessary to forward any extra parameters to BaseModel needed by classes that inherit Trader
    def __init__(self, name: str, cash: float, **args):
        super().__init__(name= name, cash=cash, **args)
        self._r = RedisService(
            os.getenv("REDIS_HOST"),
            os.getenv("REDIS_USERNAME"),
            os.getenv("REDIS_PASSWORD")
        )
        self._p = PolygonRESTService(
            os.getenv("POLYGON_API_KEY")
        )
        self._a = SchwabAccountService(debug=True)

        # function used to initialize trader values if needed
        self.on_trader_init()

    def update_trader_after_trade(self):
        pass

    def verify_order_execution(self):
        if self._a.get_order_status(self.order_id) == "Filled":
            self.awaiting_trade_confirmation = False
            self.order_id = None
            self.update_trader_after_trade()

            return "Filled"
        
        return "Waiting"
    
    def bsh(self):
        pass
    
    def update_trader(self, data):
        pass

    def on_trader_init(self):
        pass

    def get_trader_data(self):
        return self.model_dump()

    def set_message_callback(self, callback: callable):
        self._callback = callback

    def step(self):
        if self.awaiting_trade_confirmation:
            status = self.verify_order_execution()

            if status == "Waiting":
                return

        self.update_trader()
        self.bsh()