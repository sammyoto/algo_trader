from trader import Trader
from two_decimal import TwoDecimal

class Pivot_Trader(Trader):
    # buy, sell, hold
    def bsh_decision(self):
        if self.trend != "none":
            # algorithm returns decision based on data and we take action based on that
            result = self.pivot_algo()
            # take decision and execute it
            self.bsh(result)
            # final updates
            self.last_price = self.market_price
    
    def pivot_algo(self):
        delta = TwoDecimal("0.02")
        current_buy_power = (self.account_cash/self.market_price).floor()
        # we want to buy if we have no stock
        if self.current_holdings == 0:
            # buy only if the market is trending upwards
            if self.trend == "positive":
                # buy if price > pivot + delta
                if self.market_price > self.last_pivot + delta:
                    return {"action": "buy", "price": str(self.market_price) ,"quantity": str(current_buy_power), "ticker": self.ticker}
        # we want to sell
        else:
            # sell only if the market is trending downwards
            if self.trend == "negative":
                # sell if price < pivot - delta and selling higher than we bought
                if self.market_price < self.last_pivot - delta and self.market_price > self.last_action_price:
                    return {"action": "sell", "price": str(self.market_price), "quantity": str(self.current_holdings), "ticker": self.ticker}

        return {"action": "hold"}
