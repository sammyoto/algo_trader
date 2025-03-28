import os
import threading
import time
import json
from typing import List
from shared_services.redis_service import RedisService 
from shared_services.polygon_websocket_service import PolygonWebSocketService
from shared_services.polygon_rest_service import PolygonRESTService
from polygon.websocket.models import WebSocketMessage

class DataIngestionService:
    def __init__(self):
        self.r = RedisService(
            os.getenv("REDIS_HOST"),
            os.getenv("REDIS_USERNAME"),
            os.getenv("REDIS_PASSWORD")
        )
        self.pr = PolygonRESTService(
            os.getenv("POLYGON_API_KEY")
        )
        self.pw = PolygonWebSocketService(
            os.getenv("POLYGON_API_KEY")
        )
        self.pr.set_message_callback(self.process_rest_messages)
        self.pw.set_message_callback(self.process_websocket_messages)

    def process_websocket_messages(self, messages: List[WebSocketMessage]):
        for message in messages:
            print("Websocket Data", message)

    def process_rest_messages(self, messages: List[tuple]):
        for message in messages:
            message_string = json.dumps(message[1])
            self.r.publish_to_channel(channel=message[0], message=message_string)

    def run_rest_service(self):
        while True:
            try:
                self.pr.poll_subscribed_endpoints()
            except Exception as e:
                print("Error in REST service:", e)
            time.sleep(5)

    def run_websocket_service(self):
        self.pw.stream_messages()

    def start_service(self):
        rest_thread = threading.Thread(target=self.run_rest_service, name="RESTThread", daemon=True)
        websocket_thread = threading.Thread(target=self.run_websocket_service, name="WebSocketThread", daemon=True)

        rest_thread.start()
        websocket_thread.start()