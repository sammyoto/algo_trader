# Run this script when you need to generate a tokens.json file
import schwabdev

app_key = "APP KEY HERE"
secret_key = "SECRET KEY HERE"

client = schwabdev.Client(app_key, secret_key)  #create a client