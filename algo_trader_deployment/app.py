from flask import Flask
import schwabdev
import json
import os

def get_secrets():
    secrets = [os.environ.get("APP_KEY"), os.environ.get("SECRET_KEY"), os.environ.get("TOKENS")]
    return secrets

def main():
    # Grab secrets from gcp
    secrets = get_secrets()

    app_key = secrets[0]
    secret_key = secrets[1]
    tokens = json.loads(secrets[2])
    callback_url = "https://127.0.0.1"

    # Write JSON file
    with open("tokens.json", "w") as f:
        json.dump(tokens, f)

    client = schwabdev.Client(app_key, secret_key, callback_url)  #create a client
    return client.account_linked().json() #make api calls

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the root URL ('/')
@app.route('/')
def hello_world():
    temp = main()
    return temp

app.run(host="0.0.0.0", port=8080)