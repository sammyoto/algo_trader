from polygon import RESTClient
from models.polygon_models import RestEndpoint, RestEvents, RestResponseKeys
from typing import List, Callable
from urllib3 import HTTPResponse

class PolygonRESTService:
    def __init__(self, api_key):
        self.rc = RESTClient(api_key=api_key)
        self.endpoint_subs: List[RestEndpoint] = []
        self.message_callback: Callable = None

    def set_message_callback(self, callback):
        self.message_callback = callback

    def get_endpoint(self, endpoint: RestEndpoint) -> HTTPResponse:
        response_key = RestResponseKeys.get_key(endpoint.event)
        match endpoint.event:
            case RestEvents.GET_SNAPSHOT_TICKER:
                return self.rc.get_snapshot_ticker(**endpoint.params, raw=True).json()[response_key]
            case RestEvents.GET_SIMPLE_MOVING_AVERAGE:
                return self.rc.get_sma(**endpoint.params, raw=True).json()[response_key]
            case RestEvents.GET_LAST_QUOTE:
                return self.rc.get_last_quote(**endpoint.params, raw=True).json()[response_key]
            
    def delete_endpoint(self, endpoint: RestEndpoint):
        self.endpoint_subs.remove(endpoint)

    # Make an error class
    def subscribe_to_endpoint(self, endpoint: RestEndpoint):
        if endpoint not in self.endpoint_subs:
            self.endpoint_subs.append(endpoint)
            return f"Endpoint subscribed."
        return f"No duplicate endpoints."
    
    def poll_subscribed_endpoints(self):
        results = [(endpoint.get_channel_name(), self.get_endpoint(endpoint)) for endpoint in self.endpoint_subs]

        if self.message_callback:
            self.message_callback(results)
        else:
            print(results)