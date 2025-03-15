from dotenv import load_dotenv
from models.polygon_models import WebSocketEndpoint, RestEndpoint, RestEvents, WebSocketEvents, SeriesTypes, SimpleMovingAverageRestEndpoint
from services.data_ingestion_service import DataIngestionService

load_dotenv()

ws_endpoint = WebSocketEndpoint(event=WebSocketEvents.AGG_MIN, ticker="NVDA")
params = SimpleMovingAverageRestEndpoint(
    ticker='NVDA',
    series_type=SeriesTypes.HIGH,
    timespan='day',
    window=5
)
rest_endpoint = RestEndpoint(event=RestEvents.GET_SIMPLE_MOVING_AVERAGE, params=params)

d = DataIngestionService()
d.start_service()
d.pr.subscribe_to_endpoint(rest_endpoint)

while True:
    pass