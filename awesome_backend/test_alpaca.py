from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv
from datetime import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.requests import StockQuotesRequest
import os

load_dotenv()

# keys required for stock historical data client
client = StockHistoricalDataClient(os.getenv("ALPACA_BACKTESTING_API_KEY"), os.getenv("ALPACA_BACKTESTING_SECRET_KEY"))

# multi symbol request - single symbol is similar
s = StockQuotesRequest(
    symbol_or_symbols="NVDA",
    start="2025-03-01",
    end="2025-03-02"
    )

fart = client.get_stock_quotes(s)
print(fart)