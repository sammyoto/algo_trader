import json
from typing import List
from services.data_ingestion_service import DataIngestionService
from services.trader_handler_service import TraderHandlerService
from models.trader import Trader
from models.polygon_models import RestEndpoint, RestResponseKeys, WebSocketEndpoint

class ApiService:
    def __init__(self, data_ingestion_service: DataIngestionService, trader_handler_service: TraderHandlerService):
        self.data_ingestion_service = data_ingestion_service
        self.trader_handler_service = trader_handler_service

    def get_rest_endpoint(self, endpoint: RestEndpoint):
        return self.data_ingestion_service.pr.get_endpoint(endpoint)
    
    def subscribe_to_rest_endpoint(self, endpoint: RestEndpoint):
        self.data_ingestion_service.pr.subscribe_to_endpoint(endpoint)

    def delete_rest_endpoint(self, endpoint: RestEndpoint):
        self.data_ingestion_service.pr.delete_endpoint(endpoint)

    def add_trader(self, trader: Trader):
        for endpoint in trader.rest_endpoints:
            self.subscribe_to_rest_endpoint(endpoint)
        for endpoint in trader.ws_endpoints:
            self.subscribe_to_ws_endpoint(endpoint)

        self.trader_handler_service.add_trader(trader)

    def delete_trader(self, trader_name: str):
        self.trader_handler_service.delete_trader(trader_name)

    def get_all_traders(self):
        return self.trader_handler_service.get_traders()