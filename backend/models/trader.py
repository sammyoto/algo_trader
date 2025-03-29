from pydantic import BaseModel, PrivateAttr
from typing import Union, Optional, List
from shared_services.redis_service import RedisService
import threading
from models.polygon_models import RestEndpoint, WebSocketEndpoint, RestResponseType
from models.redis_models import RedisMessage
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
    
    def bsh(self):
        pass
    
    def update_trader(self):
        pass

    def step(self, data):
        print(data)

    def listen(self):
        for message in self._r.get_listener():
            if message['type'] == 'message':
                message = RedisMessage(**message)
                # we use the channel to tell what will be returned
                data = RestResponseType.get_type(message.get_data_type()).from_dict(message.data)
                self.step(message)
        
    def start(self):
        for endpoint in self.rest_endpoints:
            self._r.subscribe_to_channel(endpoint.get_channel_name())
        for endpoint in self.ws_endpoints:
            self._r.subscribe_to_channel(endpoint.endpoint_str)
        threading.Thread(target=self.listen, daemon=True).start()