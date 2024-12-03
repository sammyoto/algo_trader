import requests
import pandas as pd

# Get "data" polygon
# api_key_query = "?apiKey=b5Whl_ocnh5SvuqFCu1475WgICa9Hdiq"
# api_url = "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2023-01-09/2023-01-09"
# response = requests.get(api_url + api_key_query)
# print(response.json())

# use sample for now to test algorithm
df = pd.read_csv("data/stock_trades_sample.csv")
print(df.head())

def simulate_market_day(market_data):
    profit = 0
    bought = 0
    last_pivot = 0
    last_price = 0
    pivot_positive = True
    pivot_found = False

    bsh_delta = 0.05

    for index, row in market_data.iterrows():
        price = row["price"]

        # trading algorithm

        # first set the price and pivot point
        if index == 0:
            last_pivot = price
            last_price = price
            bought = price
        # find out which way the market will go (up or down) and set last price
        elif index == 1 or not pivot_found:
            if price == last_price:
                continue
            if price < last_price:
                pivot_positive = False
            pivot_found = True
        # make decisions based on market direction
        else:
            # update pivot if needed
            if pivot_positive:
                # sell
                if price < last_price - bsh_delta and price > bought:
                    print(f"Sold: {price}, Profit: {price - bought}")
                    profit += (price - bought)
                    last_pivot = last_price
                    bought = 0
                    pivot_positive = False
            else:
                # buy
                if price > last_price + bsh_delta:
                    print(f"Bought: {price}")
                    bought = price
                    last_pivot = last_price
                    pivot_positive = True

            # print status for debug
            print(f"Price: {price}, Last_Price: {last_price}, Last_Pivot: {last_pivot}, Profit: {profit}")

            # update last price
            last_price = price

    return profit
        

print(f"EOD Profit: {simulate_market_day(df)}")

