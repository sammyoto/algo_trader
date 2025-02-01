valid_traders = ["pivot"]

def valid_trader_ticker(trader, ticker):
    if trader in valid_traders:
        return True

    return False