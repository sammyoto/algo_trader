import json
import os
from pivot_trader import Pivot_Trader

def get_secrets():
    secrets = [os.environ.get("APP_KEY"), os.environ.get("SECRET_KEY"), os.environ.get("TOKENS")]
    return secrets

def main():
    # Grab secrets from gcp
    secrets = get_secrets()

    app_key = secrets[0]
    secret_key = secrets[1]
    tokens = json.loads(secrets[2])

    # Write JSON file
    with open("tokens.json", "w") as f:
        json.dump(tokens, f)

    bot = Pivot_Trader("NVDA", app_key, secret_key, debug=False)
    bot.start()

main()