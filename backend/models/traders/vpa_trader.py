from pydantic import PrivateAttr
from models.traders.trader import Trader
from models.two_decimal import TwoDecimal
from models.polygon_models import RestEndpoint, RestEvents, Timespan, DateFromTimestamp
from models.schwab_models import BasicOrder
from models.trader_models import VPADataSchema, VPAInitializationDataSchema
from polygon.rest.models import DailyOpenCloseAgg, Agg
from models.traders.state_models.vpa_trader_state import VPATraderState
from services.database_service import DatabaseService
from typing import List

class VPATrader(Trader):
    state: VPATraderState

    # trader state variables
    _limit: int = PrivateAttr(default=0)
    _sma_aggs: List[Agg] = PrivateAttr(default=[])
    _daily_aggs: List[DailyOpenCloseAgg] = PrivateAttr(default=[])

    def __init__(self, state: VPATraderState, db_service: DatabaseService = None, init_data: VPAInitializationDataSchema = None):
        super().__init__(
                         state=state,
                         db_service=db_service,
                         init_data=init_data
                         )

    def bsh(self):
        order: BasicOrder = None
        # compare yesterday and today to the moving average, if its lower following a high day, we buy.
        # buy signal
        if not self.state.holding:
            yesterday_index = self._limit - 2
            today_index = self._limit - 1

            yesterday_sma = self._sma_aggs[yesterday_index]
            yesterday_daily = self._daily_aggs[yesterday_index]

            today_sma = self._sma_aggs[today_index]
            today_daily = self._daily_aggs[today_index]

            yesterday_threshold = yesterday_sma.volume * (1.0 + (self.state.volume_sensitivity/100))
            today_threshold = today_sma.volume * (1.0 - (self.state.volume_sensitivity/100))

            if yesterday_daily.volume >= yesterday_threshold and today_daily.volume <= today_threshold:
                purchasable_quantity = int(self.state.cash.floored_div(self.state.current_price).root)
                order = BasicOrder(self.state.current_price, "BUY", purchasable_quantity, self.state.ticker)
            else:
                return

        # we either want to sell at our selloff percentage or our stoploss percentage
        # sell signal
        else:
            selloff_threshold = self.state.bought_price * TwoDecimal((1.0 + (self.state.selloff_percentage/100)))
            stoploss_threshold = self.state.bought_price * TwoDecimal((1.0 - (self.state.stoploss_percentage/100)))

            if self.state.current_price >= selloff_threshold or self.state.current_price <= stoploss_threshold:
                order = BasicOrder(self.state.current_price, "SELL", self.state.holdings, self.state.ticker)
            else:
                return

        # order processing
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
    
    def update_trader(self, data: VPADataSchema):
        sma = data.sma
        dailyAggs = data.dailyAggs
        quote =data.quote

        self._sma_aggs.pop(0)
        self._daily_aggs.pop(0)

        self._sma_aggs.append(sma.underlying.aggregates[0])
        self._daily_aggs.append(dailyAggs)

        if quote.ask_price and quote.bid_price:
            current_price = (quote.ask_price + quote.bid_price) / 2
            self.state.current_price = TwoDecimal(current_price)

    def get_data(self):
        sma_endpoint = RestEndpoint(RestEvents.GET_SIMPLE_MOVING_AVERAGE, {"ticker": self.state.ticker, 
                                                                           "timespan": self.state.timespan, 
                                                                           "window": self.state.window,
                                                                           "expand_underlying": True,
                                                                           "_limit": 1})
        sma_response = self._p.get_endpoint(sma_endpoint)

        daily_aggs_endpoint = RestEndpoint(RestEvents.GET_DAILY_OPEN_CLOSE_AGG, {"ticker": self.state.ticker,
                                                                                 "date": DateFromTimestamp(sma_response.values[0].timestamp)})
        daily_aggs_response = self._p.get_endpoint(daily_aggs_endpoint)

        last_quote_endpoint = RestEndpoint(RestEvents.GET_LAST_QUOTE, {"ticker": self.state.ticker})
        quote_response = self._p.get_endpoint(last_quote_endpoint)

        return VPADataSchema(sma=sma_response, dailyAggs=daily_aggs_response, quote=quote_response)
    
    # populate our lists with the moving averages and daily averages over a period of time
    def on_trader_init(self, data: VPAInitializationDataSchema):
        sma = data.sma
        daily_aggs = data.dailyAggs

        for i in range(len(sma.underlying.aggregates)):
            self._sma_aggs.append(sma.underlying.aggregates[i])
            self._daily_aggs.append(daily_aggs[i])
    
    def get_init_data(self):
        sma_endpoint = RestEndpoint(RestEvents.GET_SIMPLE_MOVING_AVERAGE, {"ticker": self.state.ticker, 
                                                                           "timespan": self.state.timespan, 
                                                                           "window": self.state.window,
                                                                           "expand_underlying": True,
                                                                           "limit": self._limit})
        sma_response = self._p.get_endpoint(sma_endpoint)
        daily_aggs = []
        for i in range(len(sma_response.values)):
            daily_aggs_endpoint = RestEndpoint(RestEvents.GET_DAILY_OPEN_CLOSE_AGG, {"ticker": self.state.ticker,
                                                                                     "date": DateFromTimestamp(sma_response.values[i].timestamp)})
            daily_aggs_response = self._p.get_endpoint(daily_aggs_endpoint)
            daily_aggs_response = self._p.get_endpoint(daily_aggs_endpoint)
            daily_aggs.append(daily_aggs_response)

        return VPAInitializationDataSchema(sma=sma_response, dailyAggs=daily_aggs)