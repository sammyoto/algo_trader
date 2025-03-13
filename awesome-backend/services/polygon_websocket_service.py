from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from models.polygon_models import WebSocketEndpoint
from typing import List, Callable, Optional

class PolygonWebSocketService:
    def __init__(self, api_key):
        self.ws = WebSocketClient(api_key=api_key)
        self.message_callback: Optional[Callable[[List[WebSocketMessage]], None]] = None

    def set_message_callback(self, callback: Callable[[List[WebSocketMessage]], None]):
        self.message_callback = callback

    def message_handler(self, messages: List[WebSocketMessage]):
        if self.message_callback:
            self.message_callback(messages)
        else:
            for m in messages:
                print(m)

    def stream_messages(self):
        self.ws.run(handle_msg=self.message_handler)

    def subscribe_to_endpoint(self, endpoint: WebSocketEndpoint):
        endpoint_str = f"{endpoint.event}.{endpoint.ticker}"
        self.ws.subscribe(endpoint_str)