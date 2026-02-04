<h1>Algo Trader</h1>
A full stack application used to create algorithmic traders.

<h2>Setup</h2>
To get started you will need the following:
<ul>
<li>Python 3.12 or newer</li>
<li>Angular CLI</li>
<li>Charles Schwab Brokerage Account</li>
<li>Coinbase Account</li>
<li>Polygon.io Subscription</li>
</ul>

<h2>Running App</h2>

You will want to have a .env file with the necessary variables set. There are a few secrets that are necessary:
```
POLYGON_API_KEY
COINBASE_API_KEY
COINBASE_SECRET_KEY
SCHWAB_API_KEY
SCHWAB_SECRET_KEY
```

Running backend
```
    source .venv/bin/activate
    cd backend
    uv run api.py
    or
    python api.py
```

Running Frontend
```
    cd frontend
    ng serve
```

<h2>Implemented Features</h2>
<ul>
<li>Two Algorithms</li>
<li>Bot lifecycle (Creation, go live, retire)</li>
<li>Bot states saved in DB</li>
<li>Connection to Coinbase</li>
</ul>

<h2>Incomplete Features</h2>
<ul>
<li>Home Page</li>
<li>Connection to Schwab</li>
<li>Backtesting</li>
</ul>

<h2>Maintenance</h2>

<h3>Tokens</h3>
Every week your Schwab tokens will expire. Once a week you will have to replace the schwab_tokens secret with a new schwab_tokens secret with the updated tokens.json. You can generate new tokens by using get_tokens.py in local_testing_example.

<h2>Page Screenshots</h2>
Home Page
<img width="2551" height="1205" alt="image" src="https://github.com/user-attachments/assets/6d8e4181-6ea5-44eb-831c-5b848dc44be0" />

Bot List
<img width="2550" height="933" alt="image" src="https://github.com/user-attachments/assets/a544c9d5-821e-4e83-b419-cd1e2094de70" />

Bot Creation
<img width="2528" height="1211" alt="image" src="https://github.com/user-attachments/assets/af368ad9-a7ef-4d4b-9811-c5369c8b1dcd" />



