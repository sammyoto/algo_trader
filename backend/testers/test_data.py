import random
from datetime import datetime, timedelta
from models.trader_models import SimpleThresholdDataSchema, VPADataSchema, VPAInitializationDataSchema
from polygon.rest.models import LastQuote, SMAIndicatorResults, DailyOpenCloseAgg

#------------------------------------------------------------------------------------------  
#                              SIMPLE THRESHOLD TRADER TEST DATA
#------------------------------------------------------------------------------------------  
mock_simple_threshold_data = [
    SimpleThresholdDataSchema(quote=LastQuote(
        ticker="NVDA",
        ask_price=200.00,
        bid_price=200.00
    )),
    SimpleThresholdDataSchema(quote=LastQuote(
        ticker="NVDA",
        ask_price=300.00,
        bid_price=300.00
    )),
    SimpleThresholdDataSchema(quote=LastQuote(
        ticker="NVDA",
        ask_price=200.00,
        bid_price=200.00
    ))
]
#------------------------------------------------------------------------------------------  
#                                   VPA TRADER TEST DATA
#------------------------------------------------------------------------------------------  
mock_vpa_init_data = VPAInitializationDataSchema(
    sma=SMAIndicatorResults(),
    dailyAggs=[
        DailyOpenCloseAgg()
    ]
)

mock_vpa_data = VPADataSchema(
    sma=SMAIndicatorResults(),
    dailyAggs=[
        DailyOpenCloseAgg()
    ],
    quote=LastQuote()
)