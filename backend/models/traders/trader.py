from pydantic import BaseModel, PrivateAttr
from typing import Union, Optional, List, Dict
from shared_services.redis_service import RedisService
from shared_services.polygon_rest_service import PolygonRESTService
from models.polygon_models import RestEndpoint, RestResponseType, RestEvents
from models.redis_models import RedisMessage
import os

class Trader(BaseModel):
    name: str
    rest_endpoints: List[RestEndpoint] = []
    _r : RedisService = PrivateAttr()
    _p : PolygonRESTService = PrivateAttr()

    def __init__(self, name: str, rest_endpoints: List[RestEndpoint]):
        super().__init__(name = name, rest_endpoints = rest_endpoints)
        self._r = RedisService(
            os.getenv("REDIS_HOST"),
            os.getenv("REDIS_USERNAME"),
            os.getenv("REDIS_PASSWORD")
        )
        self._p = PolygonRESTService()
    
    def bsh(self):
        pass
    
    def update_trader(self, data):
        pass
 
    def get_data(self):
        data = {}
        for endpoint in self.rest_endpoints:
            data[endpoint] = self._p.get_endpoint(endpoint)

        return data

    def step(self):
        self.update_trader(self.get_data())
        self.bsh()