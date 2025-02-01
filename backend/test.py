from streamer import data_streamer
import time

app_key = "GAoJ8adVvh8wkIOpGe6zIIAgVmpw6ZnK"
secret_key = "BoEhNQ1GcrMT8X4A"
tickers = ["NVDA", "AMZN", "GOOG", "BAH"]

streamer = data_streamer(app_key, secret_key, tickers)

try:
    # Start the data streamer
    streamer.start()

    # Simulate the application running
    print("Press Ctrl+C to stop...")
    while True:
        data = streamer.get_data()
        print(data)
        time.sleep(1)

except KeyboardInterrupt:
    # Stop the data streamer on interruption
    streamer.stop()
    print("Exiting application.")