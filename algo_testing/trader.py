import schwabdev
import logging
import json
from flask import Flask, render_template
from flask_socketio import SocketIO

class Trader():
    def __init__(self, ticker, app_key, secret_key, callback_url = "https://127.0.0.1", debug = True):
        self.ticker = ticker
        self.debug = debug
        self.account_cash = 500
        self.current_holdings = 0
        self.market_price = 0
        self.last_price = 0
        self.last_pivot = 0
        self.last_action_price = 0
        self.last_action = "hold"
        self.trend = "none"
        self.session_profit = 0
        self.system_message = "Nothing for now!"

        # for web server
        self.app = 0
        self.socketio = 0

        # set logging level
        logging.basicConfig(level=logging.INFO)

        # For schwabdev client
        self.client = schwabdev.Client(app_key, secret_key, callback_url)  #create a client
        self.linked_accounts = self.client.account_linked().json() # get linked account
        self.account_hash = self.linked_accounts[0].get('hashValue') # get account hash
        self.streamer = self.client.stream # create streamer

    # buy sell hold
    def bsh_decision(self):
        pass
    
    # update trader data every time a message is recieved from schwab
    def update_trader_data(self, message):
        # Ignore other messages
        if "data" in message.keys():
            content = message["data"][0]["content"][0]

            # 1 - bid and 2 - ask. Market price = bid + ask / 2. Or just use last price (3)
            if "1" in content.keys() and "2" in content.keys() and "3" in content.keys():     
                market_price = (float(content["1"]) + float(content["2"])) / 2

                self.market_price = market_price
                # start up the algorithm
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

    # return trader data
    def get_trader_data(self):
        return {"ticker": self.ticker, 
                "market_price": self.market_price,
                "last_price": self.last_price,
                "current_holdings" : self.current_holdings,
                "account_cash" : self.account_cash,
                "trend" : self.trend,
                "session_profit" : self.session_profit,
                "last_action_price" : self.last_action_price,
                "last_action" : self.last_action,
                "last_pivot" : self.last_pivot,
                "system_message": self.system_message
                }
    
    # gets called every time schwab sends us data
    def data_handler(self, message):
        json_message = json.loads(message)
        self.update_trader_data(json_message)
        self.bsh_decision()

        self.socketio.emit("update", self.get_trader_data())

    def start(self):
        # Initialize the Flask application
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)

        # Define a route for the root URL ('/')
        @self.app.route('/')
        def main():
            return render_template("index.html")

        # Start streamer, subscribe to equities
        self.streamer.start(self.data_handler)
        self.streamer.send(self.streamer.level_one_equities(self.ticker, "0,1,2,3,4,5,6,7,8"))

        # Run the app
        self.socketio.run(self.app, host="0.0.0.0", port=8080)