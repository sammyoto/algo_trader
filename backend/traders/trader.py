import logging
from traders.two_decimal import TwoDecimal

class Trader():
    def __init__(self, ticker, debug = True):
        # Set logging level
        logging.basicConfig(level=logging.INFO)

        self.ticker = ticker # The ticker we want to trade
        self.debug = debug # Set for debug mode (no real trades will be made in account)

        # Start all values at 0 for debug, in prod load previous values via load_state
        self.last_action_price = TwoDecimal("0") # Last price for buy or sell
        self.market_price = TwoDecimal("0") # Current market price
        self.last_price = TwoDecimal("0") # Previous market price
        self.last_pivot = TwoDecimal("0") # Last price the stock price pivoted at
        self.last_action = "hold" # Last action taken by trader
        self.trend = "none" # Trend of the stock price (positive or negative)
        self.session_profit = TwoDecimal("0") # Profit for the current trading session

        self.account_cash = TwoDecimal("500")
        self.current_holdings = TwoDecimal("0")

    # buy sell hold (to be updated by classes that inherit Trader)
    # Must return a bsh result
    def bsh(self):
        pass

    # def bsh(self, decision):
    #     # If we're holding don't do anything
    #     if decision["action"] == "hold":
    #         self.last_action = decision["action"]
    #         return

    #     price = TwoDecimal(decision["price"])
    #     quantity = TwoDecimal(decision["quantity"])

    #     # assuming our order gets filled at market price
    #     if self.debug:
    #         if decision["action"] == "buy":
    #             self.last_action_price = price
    #             self.current_holdings = quantity
    #             self.account_cash = self.account_cash - (price * quantity)
    #         elif decision["action"] == "sell":
    #             # profit is equal to the price * quantity - last_buy price * quantity
    #             self.session_profit = self.session_profit + (price * quantity) - (self.last_action_price * quantity)
    #             self.last_action_price = price
    #             self.current_holdings = TwoDecimal("0")
    #             self.account_cash = self.account_cash + (price * quantity)
        # # do actual orders
        # else:
        #     order_id = self.api_handler.execute_order(decision)
            
        #     # only do if order id gets returned
        #     if order_id != "No order id, order filled.":
        #         status = self.api_handler.get_order_status(order_id)

        #         # wait until order gets filled
        #         while status["status"] != "FILLED":
        #             sleep(1)
        #             status = self.api_handler.get_order_status(order_id)
                
        #         # make updates as necessary (only need to update profit when selling)
        #         fill_price = TwoDecimal(status["fill_price"])
        #         if decision["action"] == "sell":
        #             self.session_profit = self.session_profit + (fill_price * quantity) - (self.last_action_price * quantity)
        #         self.last_action_price = fill_price
        #     # if no order id (very rare) we will have to assume the fill price was at market price
        #     else:
        #         if decision["action"] == "sell":
        #             self.session_profit = self.session_profit + (price * quantity) - (self.last_action_price * quantity)
        #         self.last_action_price = price
            
        #     # update from account
        #     updates = self.api_handler.get_account_data()
        #     self.account_cash = TwoDecimal(updates["account_balance"])
        #     self.current_holdings = TwoDecimal(updates["current_holdings"])
        #     # Everytime we buy or sell, save our state in a bucket for loading
        #     self.save_state("trader-bucket-61423", "state.json", "state.json")

        # self.last_action = decision["action"]
        # self.system_message = f"Last Action: {self.last_action.upper()}, Price: {self.last_action_price}"
        
    # update trader data every time stream sends us data
    def update_trader_data(self, data):
        # 1 - bid and 2 - ask. Market price = bid + ask / 2. Or just use last price (3)
        if "1" in data.keys() and "2" in data.keys() and "3" in data.keys():
            market_price = (TwoDecimal(str(data["1"])) + TwoDecimal(str(data["2"]))) / 2

            self.market_price = market_price
            # start up the trader
            if self.last_price == 0:
                self.last_price = self.market_price
                self.last_pivot = self.market_price
            # update pivot and trend for the first time
            elif self.trend == "none":
                if self.market_price > self.last_pivot:
                    self.trend = "positive"
                else:
                    self.trend = "negative"
            else:
            # update pivot and trend each time the ticker updates if needed
                if self.market_price > self.last_price and self.trend == "negative":
                    self.last_pivot = self.last_price
                    self.trend = "positive"
                elif self.market_price < self.last_price and self.trend == "positive":
                    self.last_pivot = self.last_price
                    self.trend = "negative"

    def update_trader_after_trade(self, updates):
        if updates["action"] == "hold":
            return
        
        self.last_action = updates["action"]
        self.last_action_price = updates["last_action_price"]
        self.current_holdings = updates["current_holdings"]

    # return trader data
    def get_trader_data(self):
        return {
                "ticker": self.ticker, 
                "market_price": str(self.market_price),
                "last_price": str(self.last_price),
                "current_holdings" : str(self.current_holdings),
                "account_cash" : str(self.account_cash),
                "trend" : self.trend,
                "session_profit" : str(self.session_profit),
                "last_action_price" : str(self.last_action_price),
                "last_action" : self.last_action,
                "last_pivot" : str(self.last_pivot)
                }
    
    # gets called every time schwab sends us data
    def step(self, data):
        self.update_trader_data(data)
        result = self.bsh()
        # final updates
        self.last_price = self.market_price

        return result