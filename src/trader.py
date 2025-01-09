import schwabdev
import logging
import json
from time import sleep
from two_decimal import TwoDecimal
from api_handler import API_Handler
from flask_socketio import SocketIO, emit
from google.cloud import storage

class Trader():
    def __init__(self, socketio, ticker, app_key, secret_key, callback_url = "https://127.0.0.1", debug = True):
        self.ticker = ticker
        self.debug = debug

        # Load saved state from bucket
        self.load_state("trader-bucket-61423", "state.json", "state.json")

        self.market_price = TwoDecimal("0")
        self.last_price = TwoDecimal("0")
        self.last_pivot = TwoDecimal("0")
        self.last_action = "hold"
        self.trend = "none"
        self.session_profit = TwoDecimal("0")
        self.system_message = "Nothing for now!"

        self.socketio: SocketIO = socketio

        # set logging level
        logging.basicConfig(level=logging.INFO)

        # For schwabdev client
        self.client = schwabdev.Client(app_key, secret_key, callback_url)  #create a client
        self.linked_accounts = self.client.account_linked().json() # get linked account
        self.account_hash = self.linked_accounts[0].get('hashValue') # get account hash
        self.api_handler = API_Handler(self.client, self.account_hash) # create API handler

        # get from account
        account_data = self.api_handler.get_account_data()
        self.account_cash = TwoDecimal(account_data["account_balance"])
        self.current_holdings = TwoDecimal(account_data["current_holdings"])

        self.streamer = self.client.stream # create streamer

    # buy sell hold
    def bsh_decision(self):
        pass

    def bsh(self, decision):
        if decision["action"] == "hold":
            self.last_action = decision["action"]
            return

        if "price" in decision.keys():
            price = TwoDecimal(decision["price"])
            quantity = TwoDecimal(decision["quantity"])

        # assuming our order gets filled at market price
        if self.debug:
            if decision["action"] == "buy":
                self.last_action_price = price
                self.current_holdings = quantity
                self.account_cash = self.account_cash - (price * quantity)
            elif decision["action"] == "sell":
                self.session_profit = self.session_profit + (price * quantity) - (self.last_action_price * quantity)
                self.last_action_price = price
                self.current_holdings = TwoDecimal("0")
                self.account_cash = self.account_cash + (price * quantity)
        # do actual orders
        else:
            order_id = self.api_handler.execute_order(decision)

            # only do if order id gets returned
            if order_id != "No order id, order filled.":
                status = self.api_handler.get_order_status(order_id)

                # wait until order gets filled
                while status["status"] != "FILLED":
                    sleep(1)
                    status = self.api_handler.get_order_status(order_id)
                
                # make updates as necessary
                fill_price = TwoDecimal(status["fill_price"])
                if decision["action"] == "sell":
                    self.session_profit = self.session_profit + (fill_price * quantity) - (self.last_action_price * quantity)
                self.last_action_price = fill_price
            # if no order id (very rare) we will have to assume the fill price was at market price
            else:
                if decision["action"] == "sell":
                    self.session_profit = self.session_profit + (price * quantity) - (self.last_action_price * quantity)
                self.last_action_price = price
            
            # update from account
            updates = self.api_handler.get_account_data()
            self.account_cash = TwoDecimal(updates["account_balance"])
            self.current_holdings = TwoDecimal(updates["current_holdings"])
            # Everytime we buy or sell, save our state in a bucket for loading
            self.save_state("trader-bucket-61423", "state.json", "state.json")

        self.last_action = decision["action"]
        self.system_message = f"Last Action: {self.last_action.upper()}, Price: {self.last_action_price}"
        
    # update trader data every time a message is recieved from schwab
    def update_trader_data(self, message):
        # Ignore other messages
        if "data" in message.keys():
            content = message["data"][0]["content"][0]

            # 1 - bid and 2 - ask. Market price = bid + ask / 2. Or just use last price (3)
            if "1" in content.keys() and "2" in content.keys() and "3" in content.keys(): 
                market_price = (TwoDecimal(str(content["1"])) + TwoDecimal(str(content["2"]))) / 2
                logging.info(market_price)

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
                "last_pivot" : str(self.last_pivot),
                "system_message": self.system_message
                }
    
    def load_state(self, bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        
        blob.download_to_filename(destination_file_name)
        logging.info(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

        # Now load data from file
        with open("state.json", "r") as file:
            data = json.load(file)
        self.last_action_price = TwoDecimal(data["last_action_price"])

    def save_state(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # Initialize a Cloud Storage client
        storage_client = storage.Client()
        
        # Access the bucket
        bucket = storage_client.bucket(bucket_name)
        
        # Create a blob (object in the bucket)
        blob = bucket.blob(destination_blob_name)
        
        # Upload the file
        blob.upload_from_filename(source_file_name)
        logging.info(f"File {source_file_name} uploaded to {destination_blob_name}.")
    
    # gets called every time schwab sends us data
    def data_handler(self, message):
        json_message = json.loads(message)
        self.update_trader_data(json_message)
        self.bsh_decision()
        self.socketio.emit("update", self.get_trader_data())

    def start(self):
        # Start streamer, subscribe to equities
        self.streamer.start(self.data_handler)
        self.streamer.send(self.streamer.level_one_equities(self.ticker, "0,1,2,3,4,5,6,7,8"))