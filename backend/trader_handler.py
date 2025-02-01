from traders.trader import Trader
from traders.pivot_trader import Pivot_Trader
from traders.two_decimal import TwoDecimal
from websocket_manager import WebSocket_Manager
import asyncio

class Trader_Handler():
    def __init__(self, websocket_manager):
        self.trader_data: list[dict] = [] # ex: {trader_type: pivot, ticker: NVDA}
        self.traders: list[Trader] = []
        self.websocker_manager: WebSocket_Manager = websocket_manager

    def add_trader(self, data, debug=True):
        self.trader_data.append(data)

        if data["trader_type"] == "pivot":
            self.add_pivot_trader(data["ticker"], debug)

    def remove_trader(self, data):
        for i in range(len(self.trader_data)):
            if self.trader_data[i] == data:
                del self.trader_data[i]
                del self.traders[i]

    def execute_order(self, order, debug):
        updates = {}
        # If we're holding don't do anything
        if order["action"] == "hold":
            updates["action"] = "hold"
            return updates
          
        price = TwoDecimal(order["price"])
        quantity = TwoDecimal(order["quantity"])

        if debug:
            if order["action"] == "buy":
                updates["action"] = "buy"
                updates["last_action_price"] = price
                updates["current_holdings"] = quantity
            elif order["action"] == "sell":
                # profit is equal to the price * quantity - last_buy price * quantity
                # self.session_profit = self.session_profit + (price * quantity) - (self.last_action_price * quantity)
                updates["action"] = "sell"
                updates["last_action_price"] = price
                updates["current_holdings"] = TwoDecimal("0")

        return updates    

    # passes in content from schwab
    def pass_data(self, data):
        orders = [] 
        for stock in data:
            ticker = stock["key"] 
            for i in range(len(self.trader_data)):
                if self.trader_data[i]["ticker"] == ticker:
                    order = (i, self.traders[i].step(stock))
                    orders.append(order)
            # either wait for a response that the trade was executed, or just do a debug
            for order in orders:
                # execute the orders and wait or give the trader an update
                trader_index = order[0]
                updates = self.execute_order(order[1], self.traders[trader_index].debug)
                self.traders[trader_index].update_trader_after_trade(updates)
                self.update_subscribers(trader_index, stock)

    def get_traders_status(self):
        status = {}
        for i in range(len(self.traders)):
            trader_name = self.trader_data[i]["trader_type"] + " " + self.trader_data[i]["ticker"]
            status[trader_name] = self.traders[i].get_trader_data()
        
        return status
    
    def update_subscribers(self, trader_index, ticker_data):
        subscriber_updates = [self.traders[trader_index].get_trader_data(), ticker_data]

        asyncio.run_coroutine_threadsafe(
            self.websocker_manager.broadcast_to_subscribers(
                self.trader_data[trader_index][0],
                self.trader_data[trader_index][1],
                subscriber_updates
            ),
            loop=asyncio.get_event_loop()
        )

    def add_pivot_trader(self, ticker, debug=True):
        self.traders.append(Pivot_Trader(ticker=ticker, debug=debug))