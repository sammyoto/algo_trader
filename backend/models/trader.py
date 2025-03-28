from pydantic import BaseModel, PrivateAttr
from typing import Union, Optional, List
from shared_services.redis_service import RedisService
import threading
from models.polygon_models import RestEndpoint, WebSocketEndpoint
import os

class Trader(BaseModel):
    name: str
    rest_endpoints : List[RestEndpoint] = []
    ws_endpoints: List[WebSocketEndpoint] = []
    _r : RedisService = PrivateAttr()
    
    def __init__(self, name: str, rest_endpoints: List[RestEndpoint], ws_endpoints: List[WebSocketEndpoint]):
        super().__init__(name = name, rest_endpoints = rest_endpoints, ws_endpoints = ws_endpoints)
        self._r = RedisService(
            os.getenv("REDIS_HOST"),
            os.getenv("REDIS_USERNAME"),
            os.getenv("REDIS_PASSWORD")
        )

    def listen(self):
        for message in self._r.get_listener():
            if message['type'] == 'message':
                print(message)
        
    def start(self):
        for endpoint in self.rest_endpoints:
            self._r.subscribe_to_channel(endpoint.get_channel_name())
        for endpoint in self.ws_endpoints:
            self._r.subscribe_to_channel(endpoint.endpoint_str)
        threading.Thread(target=self.listen, daemon=True).start()