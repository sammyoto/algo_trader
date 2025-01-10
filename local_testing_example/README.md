<h1>Schwab API Local Testing</h1>

<h2>Prerequisites</h2>
From here it is assumed that you have:
<ul>
<li>Docker</li>
<li>Python 3.11 or newer</li>
<li>A Schwab Developer account (status : Ready For Use)</li>
</ul>
If you haven't set up your developer account yet you can watch the first 3 minutes of this video [here](https://www.youtube.com/watch?v=kHbom0KIJwc) by the author of the API this bot uses to get started.

<h2>Setup</h2>
<p> While it isn't necessary to have your python environment active if you're testing using docker, it's nice to have if you want to run locally without a container and we do need it to get tokens from Schwab. To get started, you first need to activate your python virtual environment and install the dependencies in algo_trader_deployment/requirements.txt.</p>

```
python3 -m venv venv

# mac/linux
source venv/bin/activate

# windows
venv\Scripts\activate

pip install -r algo_trader_deployment/requirements.txt
```

<p>You can then make a new folder named local_testing (directory name in .gitignore) and include the two scripts (get_tokens.py and local_test.sh) from this folder. Look at get_tokens.py first and fill in the variables app_key and secret_key from your schwab developer portal.</p>

```
mkdir local_testing

# mac/linux
cp local_testing_example/get_tokens.py local_testing/
cp local_testing_example/local_test.sh local_testing/

# windows
copy local_testing_example\get_tokens.py local_testing\
copy local_testing_example\local_test.sh local_testing\
```

<p>After creating a new directory, and filling in get_tokens.py, from the root directory run the get_tokens.py script first. It will have you log into your account and select the account you want tokens for. After clicking through the Schwab website, you should end up with a site can't be reached page with a url that starts with "https://127.0.0.1/?code=xxx". The program will prompt you to copy paste that url (the entire url) into the terminal. From there you can press enter and a tokens.json file should appear in your root directory.</p>

<p>From there you can now fill out local_test.sh with all the necessary information. Your file should look like this:</p>

```
docker build -t algo-trader .
docker run -p 8080:8080 \
    -e APP_KEY="APP KEY" \
    -e SECRET_KEY="SECRET KEY" \
    -e TOKENS='{
    "access_token_issued": "2025-01-10T21:05:33.311242+00:00",
    "refresh_token_issued": "2025-01-10T21:05:33.311242+00:00",
    "token_dictionary": {
        "expires_in": 1800,
        "token_type": "Bearer",
        "scope": "api",
        "refresh_token": "Blah",
        "access_token": "Blah",
        "id_token": "Blah"
        }
    }' \
    algo-trader
```

<h2>Running</h2>
<p> Before running, be sure to check that in algo_trader_deployment/app.py in the main() fuction you see:</p>

```
bot = Pivot_Trader(socketio, "NVDA", app_key, secret_key, debug=True)
```

<p>If debug is set to False the bot will start making real trades in your account with real money! From the root directory, run the local_test.sh script.</p>

```
bash local_testing/local_test.sh
```
<p>The script will build and run a docker image locally with your Schwab credentials as environment variables in the container. This mimics the setup that runs in google cloud and is a good indicator of whether or not the container will run when deployed or not. From here at http://127.0.0.1:8080/ you should see your bot running.</p>

