import json
import logging
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
from pivot_trader import Pivot_Trader

# Set up logging to stdout (console)
logging.basicConfig(level=logging.INFO)

# Initialize the Flask application
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def get_secrets():
    secrets = [os.environ.get("APP_KEY"), os.environ.get("SECRET_KEY"), os.environ.get("TOKENS")]
    return secrets

def start_bot(bot):
    bot.start()

def main():
    logging.info("Starting main function...")
    # Grab secrets from gcp
    secrets = get_secrets()

    app_key = secrets[0]
    secret_key = secrets[1]
    tokens = json.loads(secrets[2])

    # Write JSON file
    with open("tokens.json", "w") as f:
        json.dump(tokens, f)

    logging.info("Initializing bot...")
    bot = Pivot_Trader(socketio, "NVDA", app_key, secret_key, debug=False)
    bot_thread = Thread(target=start_bot, args=(bot,))
    bot_thread.daemon = True  # Ensure the thread stops when the main process exits
    bot_thread.start()
    logging.info("Bot started in the background.")

# Define a route for the root URL ('/')
@app.route('/')
def index():
    return render_template("index.html")

# Entry point for the application
if __name__ == "__main__":
    main()
    # Start the bot in the background and begin handling WebSocket connections
    socketio.run(app, host="0.0.0.0", port=8080, allow_unsafe_werkzeug=True)