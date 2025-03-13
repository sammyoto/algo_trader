from polygon import RESTClient
from models.polygon_models import RestEndpoint
from typing import List, Callable

class PolygonRESTService:
    def __init__(self, api_key):
        self.rc = RESTClient(api_key=api_key)
        self.supported_endpoints: List[str] = ["get_last_quote"]
        self.endpoint_subs: List[RestEndpoint] = []
        self.message_callback: Callable = None

    def set_message_callback(self, callback):
        self.message_callback = callback

    def get_endpoint(self, endpoint: RestEndpoint):
        match endpoint.function:
            case "get_last_quote":
                return self.rc.get_last_quote(endpoint.ticker)

    # Make an error class
    def subscribe_to_endpoint(self, endpoint: RestEndpoint):
        if endpoint.function in self.supported_endpoints:
            if endpoint not in self.endpoint_subs:
                self.endpoint_subs.append(endpoint)

                return f"Endpoint '{endpoint.function}' subscribed."
            return f"No duplicate endpoints."
        return f"Endpoint '{endpoint.function}' not supported."
    
    def poll_subscribed_endpoints(self):
        results = []
        # Make async
        for endpoint in self.endpoint_subs:
            results.append(self.get_endpoint(endpoint))

        if self.message_callback:
            self.message_callback(results)
        else:
            print(results)