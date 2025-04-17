from models.traders.trader import Trader
from models.two_decimal import TwoDecimal
from models.polygon_models import RestEndpoint, RestEvents, Timespan, DateFromTimestamp
from models.schwab_models import BasicOrder
from polygon.rest.models import DailyOpenCloseAgg, Agg
from typing import List

class VPATrader(Trader):
    ticker: str
    timespan: Timespan
    window: int
    volume_sensitivity: int
    selloff_percentage: int
    stoploss_percentage: int

    # trader state variables 
    limit: int
    sma_aggs: List[Agg]
    sma_vals: List[float]
    daily_aggs: List[DailyOpenCloseAgg]

    def __init__(self, 
                 name: str, 
                 cash: float, 
                 paper: bool,
                 ticker: str, 
                 timespan: Timespan, 
                 window: int, 
                 volume_sensitivity: int, 
                 selloff_percentage: int, 
                 stoploss_percentage: int):
        super().__init__(name=name, 
                         cash=cash, 
                         paper=paper,
                         ticker=ticker, 
                         timespan=timespan, 
                         window=window, 
                         volume_sensitivity=volume_sensitivity, 
                         selloff_percentage=selloff_percentage, 
                         stoploss_percentage = stoploss_percentage,
                         limit=3,
                         sma_aggs=[],
                         sma_vals=[],
                         daily_aggs=[]
                         )

        self.description = "A trader that trades using Volume Price Analysis."

    def bsh(self):
        order: BasicOrder = None
        # compare yesterday and today to the moving average, if its lower following a high day, we buy.
        # buy signal
        if not self.holding:
            yesterday_index = self.limit - 2
            today_index = self.limit - 1

            yesterday_agg = self.sma_aggs[yesterday_index]
            yesterday_daily = self.daily_aggs[yesterday_index]

            today_agg = self.sma_aggs[today_index]
            today_daily = self.daily_aggs[today_index]

            yesterday_threshold = yesterday_agg.volume * (1.0 + (self.volume_sensitivity/100))
            today_threshold = today_agg.volume * (1.0 - (self.volume_sensitivity/100))

            if yesterday_daily.volume >= yesterday_threshold and today_daily.volume <= today_threshold:
                purchasable_quantity = int(self.cash.floored_div(self.current_price).value)
                order = BasicOrder(self.current_price, "BUY", purchasable_quantity, self.ticker)
            else:
                return

        # we either want to sell at our selloff percentage or our stoploss percentage
        # sell signal
        else:
            selloff_threshold = self.bought_price * (1.0 + (self.selloff_percentage/100))
            stoploss_threshold = self.bought_price * (1.0 - (self.stoploss_percentage/100))

            if self.current_price >= selloff_threshold or self.current_price <= stoploss_threshold:
                order = BasicOrder(self.current_price, "SELL", self.holdings, self.ticker)
            else:
                return

        # order processing
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
        # update list with latest data, get rid of oldest data
        sma_endpoint = RestEndpoint(RestEvents.GET_SIMPLE_MOVING_AVERAGE, {"ticker": self.ticker, 
                                                                           "timespan": self.timespan, 
                                                                           "window": self.window,
                                                                           "expand_underlying": True,
                                                                           "limit": 1})
        sma_response = self._p.get_endpoint(sma_endpoint)
        daily_aggs_endpoint = RestEndpoint(RestEvents.GET_DAILY_OPEN_CLOSE_AGG, {"ticker": self.ticker,
                                                                                 "date": DateFromTimestamp(sma_response.values[0].timestamp)})
        daily_aggs_response = self._p.get_endpoint(daily_aggs_endpoint)

        self.sma_aggs.pop(0)
        self.sma_vals.pop(0)
        self.daily_aggs.pop(0)

        self.sma_aggs.append(sma_response.underlying.aggregates[0])
        self.sma_vals.append(sma_response.values[0].value)
        self.daily_aggs.append(daily_aggs_response)

        # get current price of ticker
        last_quote_endpoint = RestEndpoint(RestEvents.GET_LAST_QUOTE, {"ticker": self.ticker})
        data = self._p.get_endpoint(last_quote_endpoint)

        if data.ask_price and data.bid_price:
            current_price = (data.ask_price + data.bid_price) / 2
            self.current_price = TwoDecimal(current_price)

    # populate our lists with the moving averages and daily averages over a period of time
    def on_trader_init(self):
        sma_endpoint = RestEndpoint(RestEvents.GET_SIMPLE_MOVING_AVERAGE, {"ticker": self.ticker, 
                                                                           "timespan": self.timespan, 
                                                                           "window": self.window,
                                                                           "expand_underlying": True,
                                                                           "limit": self.limit})
        sma_response = self._p.get_endpoint(sma_endpoint)

        for i in range(len(sma_response.values)):
            self.sma_aggs.append(sma_response.underlying.aggregates[i])
            self.sma_vals.append(sma_response.values[i].value)

            daily_aggs_endpoint = RestEndpoint(RestEvents.GET_DAILY_OPEN_CLOSE_AGG, {"ticker": self.ticker,
                                                                                     "date": DateFromTimestamp(sma_response.values[i].timestamp)})
            daily_aggs_response = self._p.get_endpoint(daily_aggs_endpoint)

            self.daily_aggs.append(daily_aggs_response)