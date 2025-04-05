from models.traders.trader import Trader
from models.traders.simple_threshold_trader import SimpleThresholdTrader
from shared_services.polygon_rest_service import PolygonRESTService
from models.traders.trader import Trader
from models.two_decimal import TwoDecimal
from models.polygon_models import RestEndpoint, RestEvents, Timespan
from models.schwab_models import BasicOrder
from polygon.rest.models import SMAIndicatorResults
import os
from datetime import datetime
from time import sleep
from dotenv import load_dotenv

load_dotenv()

# trader = Trader("test", 10.0)

# tt = SimpleThresholdTrader("testing", 10.0, 10.0, 10.0, "NVDA")



p = PolygonRESTService(
            os.getenv("POLYGON_API_KEY")
        )

sma_endpoint = RestEndpoint(RestEvents.GET_SIMPLE_MOVING_AVERAGE, {"ticker": "NVDA", 
                                                                    "timespan": Timespan.DAY, 
                                                                    "window": 3,
                                                                    "expand_underlying": True,
                                                                    "limit": 1})

result: SMAIndicatorResults = p.get_endpoint(sma_endpoint)

for i in range(len(result.values)):
    agg = result.underlying.aggregates[i]
    val = result.values[i]

    dateTime = datetime.fromtimestamp(agg.timestamp / 1000)
    print(f"Agg Timestamp:{dateTime}")
    print(f"Agg:{agg}")

    dateTime = datetime.fromtimestamp(val.timestamp / 1000)
    print(dateTime.date())
    print(f"Val Timestamp:{dateTime}")
    print(f"Value:{val.value}")