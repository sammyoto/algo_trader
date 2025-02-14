import datetime
import pytz

valid_traders = ["pivot"]

def valid_trader_ticker(trader, ticker):
    if trader in valid_traders:
        return True

    return False

def get_central_timestamp():
    """Returns the current timestamp in Central Time."""

    # Get the current time in UTC
    utc_now = datetime.datetime.utcnow()

    # Define the Central Time timezone
    central_tz = pytz.timezone("America/Chicago")  # Chicago is a common city in Central Time

    # Convert the UTC time to Central Time
    central_now = utc_now.replace(tzinfo=pytz.utc).astimezone(central_tz)

    # Option 2: Return a string representation (good for display)
    return central_now.strftime("%Y-%m-%d %H:%M:%S %Z%z") # Example format

def get_date():
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")