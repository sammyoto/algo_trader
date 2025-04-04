from coinbase.rest import RESTClient
from json import dumps
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("COINBASE_API_KEY")
api_secret = os.getenv("COINBASE_SECRET_KEY")

client = RESTClient(api_key=api_key, api_secret=api_secret)

accounts = client.get_accounts()
print(dumps(accounts.to_dict(), indent=2))