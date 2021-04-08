import pandas as pd
import requests
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
UserID = 2
ReturnURL = config['WC']['returnURL']
CallbackURL = config['WC']['callbackURL']
WcVersion = config['WC']['wcVersion']
# Endpoints
AuthEndpoint = BaseURL + config['WC']['endpoints']['auth']
ProductEndpoint = BaseURL + config['WC']['endpoints']['product']

# Generate API connect variables

params = {
    "app_name": AppName,
    "scope": "read_write",
    "user_id": UserID,
    "return_url": ReturnURL,
    "callback_url": CallbackURL
}

wcAPI = API(
    url=BaseURL,
    consumer_key=ApiKey,
    consumer_secret=ApiSecret,
    version=WcVersion
)

QueryString = urlencode(params)
print(ReturnURL)
print(CallbackURL)
print("%s?%s" % (AuthEndpoint, QueryString))
