from models.traders.trader import Trader
from models.traders.simple_threshold_trader import SimpleThresholdTrader
from time import sleep
from dotenv import load_dotenv

load_dotenv()

trader = Trader("test", 10.0)

tt = SimpleThresholdTrader("testing", 10.0, 10.0, 10.0, "NVDA")

while True:
    tt.step()
    sleep(5)