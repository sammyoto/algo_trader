from models.polygon_models import Timespan
from models.traders.trader import Trader
from models.traders.simple_threshold_trader import SimpleThresholdTrader
from models.traders.vpa_trader import VPATrader
from models.two_decimal import TwoDecimal
from testers.test_data import mock_simple_threshold_data, mock_vpa_init_data, mock_vpa_data

class TraderTester:
    def __init__(self):
        pass
    def test_all_traders(self):
        self.test_trader()
        self.test_simple_threshold_trader()
        self.test_vpa_trader()

    def test_trader(self):
        trader = Trader("Test", 500, True)

        assert trader.name == "Test"
        assert trader.cash == TwoDecimal(500)
        assert trader.cash_basis == TwoDecimal(500)
        assert trader.paper == True
        assert trader.description == "Default Trader."
        assert trader.awaiting_trade_confirmation == False
        assert trader.order_id == None
        assert trader.current_order == None
        assert trader.profit == TwoDecimal(0)
        assert trader.bought_price == TwoDecimal(0)
        assert trader.current_price == TwoDecimal(0)
        assert trader.holdings == 0
        assert trader.holding == False

    def test_simple_threshold_trader(self):
        buy_threshold = 200
        sell_threshold = 300
        trader = SimpleThresholdTrader(
                                        name="Test", 
                                        cash=500, 
                                        paper=True, 
                                        buy_threshold=buy_threshold, 
                                        sell_threshold=sell_threshold, 
                                        ticker="NVDA"
                                    )

        assert trader.ticker == "NVDA"
        assert trader.buy_threshold == TwoDecimal(buy_threshold)
        assert trader.sell_threshold == TwoDecimal(sell_threshold)
        assert trader.description == "A trader that buys and sells at specific price points."

        # Uncomment when the API is available
        # trader.step()

        trader.step(mock_simple_threshold_data[0])
        assert trader.current_price == TwoDecimal(200)
        assert trader.holdings == 2
        assert trader.cash == TwoDecimal(100)
        assert trader.profit == TwoDecimal(0)
        assert trader.holding == True

        trader.step(mock_simple_threshold_data[1])
        assert trader.current_price == TwoDecimal(300)
        assert trader.holdings == 0
        assert trader.cash == TwoDecimal(700)
        assert trader.profit == TwoDecimal(200)
        assert trader.holding == False

        trader.step(mock_simple_threshold_data[2])
        assert trader.current_price == TwoDecimal(200)
        assert trader.holdings == 3
        assert trader.cash == TwoDecimal(100)
        assert trader.profit == TwoDecimal(200)
        assert trader.holding == True

    def test_vpa_trader(self):
        trader = VPATrader(name="Test", 
                           cash=500,
                           paper=True,
                           ticker="NVDA",
                           timespan=Timespan.DAY,
                           window=3,
                           volume_sensitivity=20,
                           selloff_percentage=20,
                           stoploss_percentage=20,
                           init_data=mock_vpa_init_data)
        
        assert trader.ticker == "NVDA"
        assert trader.timespan == Timespan.DAY
        assert trader.volume_sensitivity == 20
        assert trader.selloff_percentage == 20
        assert trader.stoploss_percentage == 20
        assert trader.description == "A trader that trades using Volume Price Analysis."

        # Uncomment when the API is available
        # trader.step()
        # assert trader.sma_aggs != []
        # assert trader.sma_vals != []
        # assert trader.daily_aggs != []

        trader.step(mock_vpa_data[0])
        assert trader.cash == TwoDecimal(0.00)
        assert trader.bought_price == TwoDecimal(100.00)
        assert trader.holdings == 5

        trader.step(mock_vpa_data[1])
        assert trader.cash == TwoDecimal(1000.00)
        assert trader.bought_price == TwoDecimal(0.00)
        assert trader.profit == TwoDecimal(500.00)

        trader.step(mock_vpa_data[2])
        assert trader.cash == TwoDecimal(0.00)
        assert trader.bought_price == TwoDecimal(200.00)
        assert trader.holdings == 5