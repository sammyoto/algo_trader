from polygon import RESTClient
from models.polygon_models import RestEndpoint, RestEvents, RestResponseKeys
from polygon.rest.models import modelclass
from typing import List, Callable
from urllib3 import HTTPResponse

class PolygonRESTService:
    def __init__(self, api_key):
        self.rc = RESTClient(api_key=api_key)
        self.endpoint_subs: List[RestEndpoint] = []
        self.message_callback: Callable = None

    def set_message_callback(self, callback):
        self.message_callback = callback

    def get_endpoint(self, endpoint: RestEndpoint):
        match endpoint.event:
            case RestEvents.GET_SNAPSHOT_TICKER:
                return self.rc.get_snapshot_ticker(**endpoint.params)
            case RestEvents.GET_SIMPLE_MOVING_AVERAGE:
                return self.rc.get_sma(**endpoint.params)
            case RestEvents.GET_DAILY_OPEN_CLOSE_AGG:
                return self.rc.get_daily_open_close_agg(**endpoint.params)
            case RestEvents.GET_LAST_QUOTE:
                return self.rc.get_last_quote(**endpoint.params)
            
    def delete_endpoint(self, endpoint: RestEndpoint):
        self.endpoint_subs.remove(endpoint)