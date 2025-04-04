from models.traders.trader import Trader
from models.two_decimal import TwoDecimal
from models.polygon_models import RestEndpoint, RestEvents
from models.schwab_models import BasicOrder
from polygon.rest.models import LastQuote
from typing import Union, Optional, List, Dict

class VPATrader(Trader):
    ticker: str

    # trader state variables
    current_price: TwoDecimal = TwoDecimal(0)
    holdings: int = 0
    holding: bool = False

    def __init__(self, name: str, cash: float, ticker: str):
        super().__init__(name=name, cash=cash, ticker=ticker)

        self.description = "A trader that uses Volume Price Analysis."

    def bsh(self):
        purchasable_quantity = int(self.cash.floored_div(self.current_price).value)
        order = BasicOrder(self.current_price, "BUY", purchasable_quantity, self.ticker)
        

        self.current_order = order
        self.order_id = self._a.execute_trade(order)
        status = self.verify_order_execution()

        if status == "Waiting":
            self.awaiting_trade_confirmation = True

    def update_trader_after_trade(self):
        instruction = self.current_order.get_instruction()

        if instruction == "BUY":
            self.cash -= (self.current_order.get_price() * TwoDecimal(self.current_order.get_quantity()))
            self.holdings = self.current_order.get_quantity()
        elif instruction == "SELL":
            self.cash += (self.current_order.get_price() * TwoDecimal(self.current_order.get_quantity()))
            self.holdings = self.holdings - self.current_order.get_quantity()

        self.current_order = None
    
    def update_trader(self, data: LastQuote):
        if data.ask_price and data.bid_price:
            current_price = (data.ask_price + data.bid_price) / 2
            self.current_price = TwoDecimal(current_price)
        else:
            pass
 
    def get_data(self):
        last_quote_endpoint = RestEndpoint(RestEvents.GET_LAST_QUOTE, {"ticker": self.ticker})
        response = self._p.get_endpoint(last_quote_endpoint)
        return response
    
    def get_trader_data(self):
        return self.model_dump()