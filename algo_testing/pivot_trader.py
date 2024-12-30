import math
from trader import Trader
from bsh import bsh

class Pivot_Trader(Trader):
    # buy, sell, hold
    def bsh_decision(self):
        if self.trend != "none":
            # algorithm returns decision based on data and we take action based on that
            result = self.pivot_algo()
            # take decision and execute it
            updates = bsh(result, self.last_action_price, self.client)
            # update variables
            if "last_action_price" in updates.keys():
                self.last_action = updates["last_action"]
                self.last_action_price = updates["last_action_price"]
                self.current_holdings = updates["current_holdings"]
                self.account_cash = self.account_cash + updates["account_cash_change"]
                self.session_profit = self.session_profit + updates["profit_change"]
                self.system_message = updates["message"]
            else:
                self.last_action = "hold"
            # final updates
            self.last_price = self.market_price
    
    def pivot_algo(self):
        delta = 0.02
        current_buy_power = math.floor(self.account_cash/self.market_price)
        # we want to buy if we have no stock
        if self.current_holdings == 0:
            # buy only if the market is trending upwards
            if self.trend == "positive":
                # buy if price > pivot + delta
                if self.market_price > self.last_pivot + delta:
                    return {"decision": "buy", "market_price": self.market_price ,"quantity": current_buy_power}
        # we want to sell
        else:
            # sell only if the market is trending downwards
            if self.trend == "negative":
                # sell if price < pivot - delta and selling higher than we bought
                if self.market_price < self.last_pivot - delta and self.market_price > self.last_action_price:
                    return {"decision": "sell", "market_price": self.market_price, "quantity": self.current_holdings}

        return {"decision": "hold"}
