from shared.services.redis_service import RedisService
import threading
import os

class TraderHandlerService():
    def __init__(self):
        self.r = RedisService(
            os.getenv("REDIS_HOST"),
            os.getenv("REDIS_USERNAME"),
            os.getenv("REDIS_PASSWORD")
        )
        self.r.subscribe_to_channel('get_snapshot_ticker.(market_type, stocks).(ticker, NVDA)')

    def listen(self):
        for message in self.r.get_listener():
            if message['type'] == 'message':
                print(f"Received: {message['data'].decode('utf-8')}")
        
    def start_service(self):
        threading.Thread(target=self.listen, daemon=True).start()