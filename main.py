import pandas as pd
import requests
from requests_oauthlib import OAuth1Session
from urllib.parse import urlencode
from woocommerce import API
import yaml

# Retrieve config info
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
ProductEndpoint = BaseURL + config['WC']['endpoints']['product']
OrdersEndpoint = BaseURL + config['WC']['endpoints']['orders']

# Generate API connect variables
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
test = OAuth1Session(ApiKey,
                     client_secret=ApiSecret)

# Test the OAuth1 Session
TestOrdersEndpoint = test.get(OrdersEndpoint)
TestProductEndpoint = test.get(ProductEndpoint + config['TestInfo']['TestProductID'])

# Works!
print(TestOrdersEndpoint.json())
print(TestProductEndpoint.json())


