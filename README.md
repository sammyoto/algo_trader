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