from testers.trader_tester import TraderTester
from dotenv import load_dotenv

load_dotenv()

tester = TraderTester()
tester.test_all_traders()
print("All tests passed.")