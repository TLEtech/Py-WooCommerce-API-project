import pandas as pd
import json
import requests
from requests_oauthlib import OAuth1Session
from urllib.parse import urlencode
from woocommerce import API
import yaml

# Retrieve config info - fill out config.example.yml as needed, and rename it to config.yml
with open("config.yml", 'r') as configInfo:
    config = yaml.safe_load(configInfo)

# Set variables
ApiKey = config['WC']['apiKey']
ApiSecret = config['WC']['apiSecret']
AppName = config['WC']['appName']
BaseURL = config['WC']['baseURL']
UserID = config['WC']['userID']
ReturnURL = config['WC']['returnURL']
CallbackURL = config['WC']['callbackURL']
WcVersion = config['WC']['wcVersion']

# Endpoints
AuthEndpoint = BaseURL + config['WC']['endpoints']['auth']
ProductsEndpoint = BaseURL + config['WC']['endpoints']['products']
OrdersEndpoint = BaseURL + config['WC']['endpoints']['orders']
CategoriesEndpoint = BaseURL + config['WC']['endpoints']['categories']

# We will be using Oauth1 for the purposes of this solution, so we do not need to
# worry about utilizing API callbacks just yet. I will provide the info in case
# we want to come back to it later.

# Generate API connect variables for automated key generation, if needed later
params = {
    "app_name": AppName,
    "scope": "read_write",
    "user_id": UserID,
    "return_url": ReturnURL,
    "callback_url": CallbackURL
}

# For HTTP Basic Auth
wcAPI = API(
    url=BaseURL,
    consumer_key=ApiKey,
    consumer_secret=ApiSecret,
    version=WcVersion
)

# If API Callback is needed (for automated key generation), we can print out and follow the KeyURL.
QueryString = urlencode(params)
KeyURL = ("%s?%s" % (AuthEndpoint, QueryString))

# Create OAuth1 Session
Retrieve = OAuth1Session(ApiKey,
                         client_secret=ApiSecret)

# In Progress
print(Retrieve.get(CategoriesEndpoint).json())
