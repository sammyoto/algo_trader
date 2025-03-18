from pydantic import BaseModel, PrivateAttr
from typing import Union, Optional, List
import json
import os
import threading
from enum import Enum
from models.polygon_models import RestEndpoint, WebSocketEndpoint
from services.redis_service import RedisService

class TraderAlgorithm(str, Enum):
    PIVOT = "pivot"

class Trader(BaseModel):
    algorithm: TraderAlgorithm
    rest_endpoints: List[RestEndpoint]
    websocket_endpoints: List[WebSocketEndpoint]

    # private attribute, not part of pydantic model validation
    _r: RedisService = PrivateAttr(default=None)
    _listener_thread: Optional[threading.Thread] = PrivateAttr(default=None)

    def __init__(self,
                 algorithm: TraderAlgorithm, 
                 rest_endpoints: List[RestEndpoint], 
                 websocket_endpoints: List[WebSocketEndpoint]):
        
        super().__init__(algorithm=algorithm,
                         rest_endpoints=rest_endpoints, 
                         websocket_endpoints=websocket_endpoints,
                         )
        
        self._r = RedisService(os.getenv("REDIS_HOST"),os.getenv("REDIS_USERNAME"),os.getenv("REDIS_PASSWORD"))
        
    def listen(self):
        for endpoint in self.rest_endpoints:
            self._r.subscribe_to_channel(endpoint.get_channel_name())
        
        def listener():
            # This loop will run indefinitely.
            for message in self._r.get_listener():
                self.handle_message(message)

        self._listener_thread = threading.Thread(target=listener, daemon=True)
        self._listener_thread.start()

    def handle_message(self, message):
        print(f"Trader: {message}")

    def update(self):
        pass

    def bsh(self):
        pass

    def order(self):
        pass

    def step(self):
        self.update()
        self.order(self.bsh())