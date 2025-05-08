from models.traders.trader import Trader
from models.two_decimal import TwoDecimal
from models.polygon_models import RestEndpoint, RestEvents
from models.schwab_models import BasicOrder
from models.trader_models import SimpleThresholdDataSchema
from models.traders.state_models.simple_threshold_trader_state import SimpleThresholdTraderState
from polygon.rest.models import LastQuote
from typing import Union, Optional, List, Dict
from services.database_service import DatabaseService

class SimpleThresholdTrader(Trader):
    state: SimpleThresholdTraderState

    def __init__(self, state: SimpleThresholdTraderState, db_service: DatabaseService = None, init_data: SimpleThresholdDataSchema = None):
        super().__init__(state=state, db_service=db_service, init_data=init_data)

    def bsh(self):
        purchasable_quantity = int(self.state.cash.floored_div(self.state.current_price).root)
        
        if not self.state.holding and self.state.current_price <= self.state.buy_threshold:
            order = BasicOrder(self.state.current_price, "BUY", purchasable_quantity, self.state.ticker)
        elif self.state.holding and self.state.current_price >= self.state.sell_threshold:
            order = BasicOrder(self.state.current_price, "SELL", self.state.holdings, self.state.ticker)
        else:
            return

        self._current_order = order
        self.state.order_id = self._a.execute_trade(order)
        status = self.verify_order_execution()

        if status == "Waiting":
            self.state.awaiting_trade_confirmation = True

    def update_trader_after_trade(self):
        instruction = self._current_order.get_instruction()

        if instruction == "BUY":
            self.state.cash -= (self._current_order.get_price() * TwoDecimal(self._current_order.get_quantity()))
            self.state.bought_price = self._current_order.get_price()
            self.state.holdings = self._current_order.get_quantity()
            self.state.holding = True
        elif instruction == "SELL":
            self.state.cash += (self._current_order.get_price() * TwoDecimal(self._current_order.get_quantity()))
            self.state.profit += ((self._current_order.get_price() * TwoDecimal(self._current_order.get_quantity())) - (self.state.bought_price * TwoDecimal(self._current_order.get_quantity())))
            self.state.bought_price = TwoDecimal(0)
            self.state.holdings = self.state.holdings - self._current_order.get_quantity()
            self.state.holding = False

        self._current_order = None
    
    def update_trader(self, data: SimpleThresholdDataSchema):
        quote = data.quote
        if quote.ask_price and quote.bid_price:
            current_price = (quote.ask_price + quote.bid_price) / 2
            self.state.current_price = TwoDecimal(current_price)
        else:
            pass

    def get_data(self):
        last_quote_endpoint = RestEndpoint(RestEvents.GET_LAST_QUOTE, {"ticker": self.state.ticker})
        data = self._p.get_endpoint(last_quote_endpoint)
        return SimpleThresholdDataSchema(quote=data)