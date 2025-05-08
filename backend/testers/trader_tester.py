from models.polygon_models import Timespan
from models.traders.trader import Trader
from models.traders.simple_threshold_trader import SimpleThresholdTrader
from models.traders.vpa_trader import VPATrader
from models.traders.state_models.trader_state import TraderState
from models.traders.state_models.simple_threshold_trader_state import SimpleThresholdTraderState
from models.traders.state_models.vpa_trader_state import VPATraderState
from services.database_service import DatabaseService
from models.two_decimal import TwoDecimal
from testers.test_data import mock_simple_threshold_data, mock_vpa_init_data, mock_vpa_data

class TraderTester:
    def __init__(self):
        self._d = DatabaseService()
    def test_all_traders(self):
        self.test_trader()
        self.test_simple_threshold_trader()
        self.test_vpa_trader()

    def test_trader(self):
        state = TraderState(name="Test", cash=TwoDecimal(500), cash_basis=TwoDecimal(500), paper=True)
        trader = Trader(state=state)

        assert trader.state.name == "Test"
        assert trader.state.cash == TwoDecimal(500)
        assert trader.state.cash_basis == TwoDecimal(500)
        assert trader.state.paper == True
        assert trader.state.description == "Trader Base Model."
        assert trader.state.awaiting_trade_confirmation == False
        assert trader.state.order_id == None
        assert trader.state.profit == TwoDecimal(0)
        assert trader.state.bought_price == TwoDecimal(0)
        assert trader.state.current_price == TwoDecimal(0)
        assert trader.state.holdings == 0
        assert trader.state.holding == False

    def test_simple_threshold_trader(self):
        buy_threshold = TwoDecimal(200)
        sell_threshold = TwoDecimal(300)
        
        state = SimpleThresholdTraderState(name="SimpleTest",
                                           cash=TwoDecimal(500),
                                           cash_basis=TwoDecimal(500),
                                           paper=True,
                                           buy_threshold=buy_threshold, 
                                           sell_threshold=sell_threshold, 
                                           ticker="NVDA")
        state = self._d.push_trader_state(state)
        trader = SimpleThresholdTrader(state=state, db_service=self._d)

        print(trader.state)

        assert trader.state.ticker == "NVDA"
        assert trader.state.buy_threshold == buy_threshold
        assert trader.state.sell_threshold == sell_threshold
        assert trader.state.description == "A trader that buys and sells at specific price points."
        assert trader.state.awaiting_trade_confirmation == False

        trader.step(mock_simple_threshold_data[0])
        assert trader.state.current_price == TwoDecimal(200)
        assert trader.state.holdings == 2
        assert trader.state.cash == TwoDecimal(100)
        assert trader.state.profit == TwoDecimal(0)
        assert trader.state.holding == True

        trader.step(mock_simple_threshold_data[1])
        assert trader.state.current_price == TwoDecimal(300)
        assert trader.state.holdings == 0
        assert trader.state.cash == TwoDecimal(700)
        assert trader.state.profit == TwoDecimal(200)
        assert trader.state.holding == False

        trader.step(mock_simple_threshold_data[2])
        assert trader.state.current_price == TwoDecimal(200)
        assert trader.state.holdings == 3
        assert trader.state.cash == TwoDecimal(100)
        assert trader.state.profit == TwoDecimal(200)
        assert trader.state.holding == True

    def test_vpa_trader(self):
        state = VPATraderState(
                            name="Test", 
                            cash=TwoDecimal(500),
                            cash_basis=TwoDecimal(500),
                            paper=True,
                            ticker="NVDA",
                            timespan=Timespan.DAY,
                            window=3,
                            volume_sensitivity=20,
                            selloff_percentage=20,
                            stoploss_percentage=20
                           )
        state = self._d.push_trader_state(state)
        trader = VPATrader(state=state, db_service=self._d, init_data=mock_vpa_init_data)
        
        print(trader.state)

        assert trader.state.ticker == "NVDA"
        assert trader.state.timespan == Timespan.DAY
        assert trader.state.volume_sensitivity == 20
        assert trader.state.selloff_percentage == 20
        assert trader.state.stoploss_percentage == 20
        assert trader.state.description == "A trader that trades using Volume Price Analysis."

        # Uncomment when the API is available
        # trader.step()
        # assert trader.sma_aggs != []
        # assert trader.sma_vals != []
        # assert trader.daily_aggs != []

        trader.step(mock_vpa_data[0])
        assert trader.state.cash == TwoDecimal(0.00)
        assert trader.state.bought_price == TwoDecimal(100.00)
        assert trader.state.holdings == 5

        trader.step(mock_vpa_data[1])
        assert trader.state.cash == TwoDecimal(1000.00)
        assert trader.state.bought_price == TwoDecimal(0.00)
        assert trader.state.profit == TwoDecimal(500.00)

        trader.step(mock_vpa_data[2])
        assert trader.state.cash == TwoDecimal(0.00)
        assert trader.state.bought_price == TwoDecimal(200.00)
        assert trader.state.holdings == 5