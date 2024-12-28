import math
def pivot_bsh(market_data):
    delta = 0.02
    current_buy_power = math.floor(market_data["account_cash"]/market_data["market_price"])
    # we want to buy if we have no stock
    if market_data["current_holdings"] == 0:
        # buy only if the market is trending upwards
        if market_data["trend"] == "positive":
            # buy if price > pivot + delta
            if market_data["market_price"] > market_data["last_pivot"] + delta:
                return {"decision": "buy", "market_price": market_data["market_price"] ,"quantity": current_buy_power}
    # we want to sell
    else:
        # sell only if the market is trending downwards
        if market_data["trend"] == "negative":
            # sell if price < pivot - delta and selling higher than we bought
            if market_data["market_price"] < market_data["last_pivot"] - delta and market_data["market_price"] > market_data["last_action_price"]:
                return {"decision": "sell", "market_price": market_data["market_price"], "quantity": market_data["current_holdings"]}

    return {"decision": "hold"}