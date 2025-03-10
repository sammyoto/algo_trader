from polygon import RESTClient
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from typing import List

api_key = "b5Whl_ocnh5SvuqFCu1475WgICa9Hdiq"

c = WebSocketClient(subscriptions=["T.*"], api_key=api_key)

def handle_msg(msgs: List[WebSocketMessage]):
    for m in msgs:
        print(m)

c.run(handle_msg)