class Schwab_Data_Object():
    def __init__(self, ticker_data):
        self.tickers = [stock["key"] for stock in ticker_data]
        self.ticker_data = {stock["key"]: stock for stock in ticker_data}

    def get_tickers(self):
        return self.tickers
    
    def get_ticker_data(self, ticker):
        return self.ticker_data[ticker]