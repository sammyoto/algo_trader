from models.traders.simple_threshold_trader import SimpleThresholdTrader
from models.traders.vpa_trader import VPATrader
from models.polygon_models import Timespan
from models.two_decimal import TwoDecimal
from dotenv import load_dotenv

load_dotenv()

def test_simple_threshold_trader():
    trader = SimpleThresholdTrader("Test", 500, 500, 500, 'NVDA')

    assert trader.cash == TwoDecimal(500)

def test_vpa_trader():
    trader = VPATrader("Test", 
                       500, 
                       "NVDA",
                        Timespan.DAY,
                        3,
                        20,
                        20,
                        20)
    
    assert trader.cash == TwoDecimal(500)
    assert trader.selloff_percentage == 20
    assert trader.stoploss_percentage == 20

    

test_simple_threshold_trader()
test_vpa_trader()