def bsh(algo_result, last_action_price, client):
    # for testing, will put in real orders later
    if algo_result["decision"] == "buy":
        # assuming our order gets filled at market price
        print("buy")
        return {"last_action": algo_result["decision"],
                "last_action_price": algo_result["market_price"],
                "current_holdings": algo_result["quantity"],
                "account_cash_change": -(algo_result["market_price"] * algo_result["quantity"]),
                "profit_change": 0,
                "message": f"Last bought at ${algo_result['market_price']}"
               }
    elif algo_result["decision"] == "sell":
        print("sell")
        return {"last_action": algo_result["decision"],
                "last_action_price": algo_result["market_price"],
                "current_holdings": 0,
                "account_cash_change": algo_result["market_price"] * algo_result["quantity"],
                "profit_change": (algo_result["market_price"] * algo_result["quantity"]) - (last_action_price * algo_result["quantity"]),
                "message": f"Last sold at ${algo_result['market_price']}"
               }
    else:
        return {}