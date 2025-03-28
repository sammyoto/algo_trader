from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, EquityAgg
from models.polygon_models import WebSocketEndpoint
from typing import List, Callable, Optional
import json

class PolygonWebSocketService:
    def __init__(self, api_key):
        self.ws = WebSocketClient(api_key=api_key)
        self.endpoint_subs: List[WebSocketEndpoint] = []
        self.message_callback: Optional[Callable[[List[WebSocketMessage]], None]] = None

    def set_message_callback(self, callback: Callable[[List[WebSocketMessage]], None]):
        self.message_callback = callback

    def message_handler(self, messages: str):
        if self.message_callback:
            messages = json.loads(messages)
            self.message_callback(messages)
        else:
            for m in messages:
                print(m)

    def stream_messages(self):
        self.ws.run(handle_msg=self.message_handler)

    def subscribe_to_endpoint(self, endpoint: WebSocketEndpoint):
        self.ws.subscribe(endpoint.endpoint_str)
        self.endpoint_subs.append(endpoint)