from traders.trader import Trader
from traders.pivot_trader import Pivot_Trader
from traders.two_decimal import TwoDecimal
from websocket_manager import WebSocket_Manager
from schwab_data_object import Schwab_Data_Object
from helper_functions import get_central_timestamp
import asyncio

class Trader_Handler():
    def __init__(self, websocket_manager):
        self.traders: list[Trader] = [] # ex: {trader_type: pivot, ticker: NVDA, trader: Trader()}
        self.websocket_manager: WebSocket_Manager = websocket_manager
        self.session_history = []

    def add_trader(self, data, debug=True):
        # don't allow traders of the same type and ticker (no duplicates)
        if self.get_trader_by_data(data) != "Trader not found.":
            return "Can't add duplicate traders."
        if data["trader_type"] == "pivot":
            self.add_pivot_trader(data["ticker"], debug)

    def get_trader_by_data(self, data):
        for trader in self.traders:
            trader_metadata = {"trader_type": trader.trader_type, "ticker": trader.ticker}
            if trader_metadata == data:
                return trader
        
        return "Trader not found."
    
    def get_trader_by_index(self, index):
        if index > len(self.traders) - 1 or index < 0:
            return "Not a valid index."
        
        return self.traders[index]
    
    def get_traders_by_ticker(self, ticker):
        traders = []
        for trader in self.traders:
            if trader.ticker == ticker:
                traders.append(trader)
        
        return traders
    
    def get_traders_by_type(self, trader_type):
        traders = []
        for trader in self.traders:
            if trader.trader_type == trader_type:
                traders.append(trader)
        
        return traders

    def remove_trader(self, data):
        for trader in self.traders:
            trader_metadata = {"trader_type": trader.trader_type, "ticker": trader.ticker}
            if trader_metadata == data:
                self.traders.remove(trader)

    def get_traders_status(self):
        status = {}
        for trader in self.traders:
            trader_name = trader.trader_type + " " + trader.ticker
            status[trader_name] = trader.get_trader_data()
        
        return status
    
    def add_pivot_trader(self, ticker, debug=True):
        self.traders.append(Pivot_Trader(ticker=ticker, debug=debug))

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
    def pass_data(self, schwab_data: Schwab_Data_Object):
        tick_data = {
            "timestamp": get_central_timestamp(),
            "schwab_data": schwab_data,
            "trader_activity": {}
        }
        for ticker in schwab_data.get_tickers():
            orders = [] 
            ticker_data = schwab_data.get_ticker_data(ticker)
            for trader in self.get_traders_by_ticker(ticker):
                tick_data["trader_activity"][trader.get_name()] = {"trader_data": trader.get_trader_data()}
                order = (trader, trader.step(ticker_data))
                orders.append(order)
            # either wait for a response that the trade was executed, or just do a debug
            for order in orders:
                # execute the orders and wait or give the trader an update
                trader = order[0]
                tick_data["trader_activity"][trader.get_name()]["order"] = order
                updates = self.execute_order(order[1], trader.debug)
                trader.update_trader_after_trade(updates)
                self.update_subscribers(trader, schwab_data.get_ticker_data(ticker))
                
        self.session_history.append(tick_data)

    def update_subscribers(self, trader, ticker_data):
        subscriber_updates = {"trader_data": trader.get_trader_data(),
                              "ticker_data": ticker_data}

        asyncio.run_coroutine_threadsafe(
            self.websocket_manager.broadcast_to_subscribers(
                trader.trader_type,
                trader.ticker,
                subscriber_updates
            ),
            loop=asyncio.get_event_loop()
        )