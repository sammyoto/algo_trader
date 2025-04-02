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

    def __init__(self, name, buy_threshold, sell_threshold, ticker):
        super.__init__(name = name, buy_threshold = buy_threshold, sell_threshold = sell_threshold, ticker = ticker)
        self._description = "A trader that buys and sells at specific price points."

        # trader state variables
        self.current_price: TwoDecimal = TwoDecimal(0)
        self.holdings: int = 0
        self.holding: bool = False

    def bsh(self):
        purchasable_quantity = int(self.cash.floored_div(self.current_price).value)

        if not self.holding and self.current_price < self.buy_threshold:
            order = BasicOrder(self.current_price, "BUY", purchasable_quantity, self.ticker)
        elif self.holding and self.current_price > self.sell_threshold:
            order = BasicOrder(self.current_price, "SELL", self.holdings, self.ticker)
        else:
            return

        self.order_id = self._a.execute_trade(order)
        status = self.verify_order_execution()

        if status == "Waiting":
            self.awaiting_trade_confirmation = True

    def update_trader_after_trade(self):
        pass
    
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