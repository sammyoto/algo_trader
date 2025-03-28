import json
from typing import List
from services.data_ingestion_service import DataIngestionService
from services.trader_handler_service import TraderHandlerService
from models.trader import Trader
from models.polygon_models import RestEndpoint, RestResponseKeys

class ApiService:
    def __init__(self, data_ingestion_service: DataIngestionService, trader_handler_service: TraderHandlerService):
        self.data_ingestion_service = data_ingestion_service
        self.trader_handler_service = trader_handler_service

    def get_rest_endpoint(self, endpoint: RestEndpoint):
        return self.data_ingestion_service.pr.get_endpoint(endpoint)
    
    def subscribe_to_rest_endpoint(self, endpoint: RestEndpoint):
        self.data_ingestion_service.pr.subscribe_to_endpoint(endpoint)

    def add_trader(self, trader: Trader):
        for endpoint in trader.rest_endpoints:
            self.data_ingestion_service.pr.subscribe_to_endpoint(endpoint)
        self.trader_handler_service.add_trader(trader)