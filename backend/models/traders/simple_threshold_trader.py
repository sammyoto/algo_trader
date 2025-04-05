from models.traders.trader import Trader
from models.two_decimal import TwoDecimal
from models.polygon_models import RestEndpoint, RestEvents
from models.schwab_models import BasicOrder
from polygon.rest.models import LastQuote
from typing import Union, Optional, List, Dict

class SimpleThresholdTrader(Trader):
    buy_threshold: TwoDecimal
    sell_threshold: TwoDecimal
    ticker: str

    # trader state variables
    profit: TwoDecimal = TwoDecimal(0)
    bought_price: TwoDecimal = TwoDecimal(0)
    current_price: TwoDecimal = TwoDecimal(0)
    holdings: int = 0
    holding: bool = False

    def __init__(self, name: str, cash: float, buy_threshold: float, sell_threshold: float, ticker: str):
        super().__init__(name=name, cash=cash, buy_threshold=buy_threshold, sell_threshold=sell_threshold, ticker=ticker)

        self.description = "A trader that buys and sells at specific price points."

    def bsh(self):
        purchasable_quantity = int(self.cash.floored_div(self.current_price).value)

        if not self.holding and self.current_price < self.buy_threshold:
            order = BasicOrder(self.current_price, "BUY", purchasable_quantity, self.ticker)
        elif self.holding and self.current_price > self.sell_threshold:
            order = BasicOrder(self.current_price, "SELL", self.holdings, self.ticker)
        else:
            return

        self.current_order = order
        self.order_id = self._a.execute_trade(order)
        status = self.verify_order_execution()

        if status == "Waiting":
            self.awaiting_trade_confirmation = True

    def update_trader_after_trade(self):
        instruction = self.current_order.get_instruction()

        if instruction == "BUY":
            self.cash -= (self.current_order.get_price() * TwoDecimal(self.current_order.get_quantity()))
            self.bought_price = self.current_order.get_price()
            self.holdings = self.current_order.get_quantity()
            self.holding = True
        elif instruction == "SELL":
            self.cash += (self.current_order.get_price() * TwoDecimal(self.current_order.get_quantity()))
            self.profit += ((self.current_order.get_price() * TwoDecimal(self.current_order.get_quantity())) - self.bought_price)
            self.bought_price = TwoDecimal(0)
            self.holdings = self.holdings - self.current_order.get_quantity()
            self.holding = False

        self.current_order = None
    
    def update_trader(self):
        last_quote_endpoint = RestEndpoint(RestEvents.GET_LAST_QUOTE, {"ticker": self.ticker})
        data = self._p.get_endpoint(last_quote_endpoint)

        if data.ask_price and data.bid_price:
            current_price = (data.ask_price + data.bid_price) / 2
            self.current_price = TwoDecimal(current_price)
        else:
            pass