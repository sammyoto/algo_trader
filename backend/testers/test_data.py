import random
from datetime import datetime, timedelta
from models.trader_models import SimpleThresholdDataSchema, VPADataSchema, VPAInitializationDataSchema
from polygon.rest.models import LastQuote, SMAIndicatorResults, DailyOpenCloseAgg, IndicatorUnderlying, Agg

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
    sma=SMAIndicatorResults(
        underlying=IndicatorUnderlying(
            aggregates=[
                Agg(
                    volume=100
                ),
                Agg(
                    volume=100
                ),
                Agg(
                    volume=100
                )
            ]
        )
        ),
    dailyAggs=[
        DailyOpenCloseAgg(volume=100),
        DailyOpenCloseAgg(volume=100),
        DailyOpenCloseAgg(volume=200)
    ]
)

mock_vpa_data = [
    VPADataSchema(
    sma=SMAIndicatorResults(
        underlying=IndicatorUnderlying(
            aggregates=[
                Agg(
                    volume=100
                )
            ]
        )
    ),
    dailyAggs=DailyOpenCloseAgg(volume=50),
    quote=LastQuote(
        ticker="NVDA",
        ask_price=100.00,
        bid_price=100.00
    )
    ),
    VPADataSchema(
    sma=SMAIndicatorResults(
        underlying=IndicatorUnderlying(
            aggregates=[
                Agg(
                    volume=100
                )
            ]
        )
    ),
    dailyAggs=DailyOpenCloseAgg(volume=150),
    quote=LastQuote(
        ticker="NVDA",
        ask_price=200.00,
        bid_price=200.00
    )
    ),
    VPADataSchema(
    sma=SMAIndicatorResults(
        underlying=IndicatorUnderlying(
            aggregates=[
                Agg(
                    volume=100
                )
            ]
        )
    ),
    dailyAggs=DailyOpenCloseAgg(volume=50),
    quote=LastQuote(
        ticker="NVDA",
        ask_price=200.00,
        bid_price=200.00
    )
    )
]