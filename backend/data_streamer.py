import schwabdev
import json
from threading import Thread
from websocket_manager import WebSocket_Manager
from api_handlers.schwab_api_handler import Schwab_API_Handler
from trader_handler import Trader_Handler
from schwab_data_object import Schwab_Data_Object

traders = [{"trader_type": "pivot", "ticker" : "NVDA"},
           {"trader_type": "pivot", "ticker" : "AMZN"},
           {"trader_type": "pivot", "ticker" : "GOOG"},
           {"trader_type": "pivot", "ticker" : "BAH"}
           ]

class Data_Streamer(): 
    def __init__(self, app_key, secret_key, tickers, websocket_manager: WebSocket_Manager):
        self.app_key = app_key
        self.secret_key = secret_key
        self.tickers = tickers
        self.client = schwabdev.Client(self.app_key, self.secret_key, callback_url = "https://127.0.0.1")  # create a client
        self.linked_accounts = self.client.account_linked().json()  # Get linked account
        self.account_hash = self.linked_accounts[0].get('hashValue')  # Get account hash

        self.websocket_manager = websocket_manager
        self.api_handler = Schwab_API_Handler(self.client, self.account_hash)
        self.trader_handler = Trader_Handler(self.websocket_manager)
        # temporary, add traders to trader handler
        for trader in traders:
            self.trader_handler.add_trader(trader)
        self.streamer = None

        self.thread = None
        
    # gets called every time schwab sends us data
    def data_handler(self, message):
        json_message = json.loads(message)
        print(json_message)

        if "data" in json_message.keys():
            schwab_data = Schwab_Data_Object(json_message["data"][0]["content"])
            self.trader_handler.pass_data(schwab_data)
 
    def stream(self):
        self.streamer = self.client.stream
        self.streamer.start(self.data_handler)
        self.streamer.send(self.streamer.level_one_equities(self.tickers, "0,1,2,3,4,5,6,7,8"))
        
    # to thread so we don't interrupt API thread
    def start(self):
        self.thread = Thread(target=self.stream, daemon=True)
        self.thread.start()

    def stop(self):
        # shouldn't need since thread is daemon but just in case
        if self.thread and self.thread.is_alive():
            self.thread.join()  # Wait for the thread to finish
            print("Data streamer stopped.")
        else:
            print("Data streamer is not running.")