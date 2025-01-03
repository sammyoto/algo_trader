import json

class API_Handler():
    def __init__(self, client, account_hash):
        self.client = client
        self.account_hash = account_hash

        # Load file into memory so we don't have to read file every order
        # Specify the file path
        file_path = 'schwab_api_json_templates/order.json'

        # Open the file and load the JSON data
        with open(file_path, 'r') as file:
            account_order = json.load(file)
        self.account_order = account_order
    
    def get_account_data(self):
        client_json = self.client.account_details(self.account_hash, fields="positions").json()

        account_balance = client_json["securitiesAccount"]["currentBalances"]["cashBalance"]

        # can only access if we hold any equities
        if "positions" in client_json["securitiesAccount"].keys():
            ticker_data = client_json["securitiesAccount"]["positions"][0]
            current_holdings = ticker_data["longQuantity"]
            return {"account_balance": account_balance, "current_holdings": current_holdings}
        
        return {"account_balance": account_balance, "current_holdings": 0}
    
    def execute_order(self, order):
        # create order
        self.account_order["price"] = order["price"]
        self.account_order["orderLegCollection"][0]["instruction"] = order["action"].upper()
        self.account_order["orderLegCollection"][0]["quantity"] = order["quantity"]
        self.account_order["orderLegCollection"][0]["instrument"]["symbol"] = order["ticker"]

        resp = self.client.order_place(self.account_hash, self.account_order)
        # get response id
        try:
            order_id = resp.headers.get('location', '/').split('/')[-1]
            return order_id
        except:
            return "No order id, order filled."

    def get_order_status(self, order_id):
        response = self.client.order_details(self.account_hash, order_id).json()

        # price only exists if order is filled
        if response["status"] == "FILLED":
            return {"status": response["status"], "fill_price": response["orderActivityCollection"][0]["executionLegs"][0]["price"]}

        return {"status": response["status"], "fill_price": 0}