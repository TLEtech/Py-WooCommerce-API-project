import pandas as pd
import json
import requests
from requests import utils
from requests_oauthlib import OAuth1Session, OAuth1
from urllib.parse import urlencode
from woocommerce import API
import yaml
import data

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
Filter_Products = config['ETL']['FilterPrice']
PriceParams = {'status': 'publish',
               'type': 'variable',
               'per_page': 50}

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
    version=WcVersion,
    wp_api=True
)

# If API Callback is needed (for automated key generation), we can print out and follow the KeyURL.
QueryString = urlencode(params)
KeyURL = ("%s?%s" % (AuthEndpoint, QueryString))

# Create OAuth1 Session
# Retrieve = OAuth1Session(ApiKey, client_secret=ApiSecret)
AppAuth = OAuth1(ApiKey, ApiSecret)

# In Progress
LocalPriceDF = data.df
LocalPriceJSON = LocalPriceDF.to_json(orient="records")

WebsitePriceList = (requests.get(ProductsEndpoint, auth=AppAuth, params=PriceParams).json())
WebsitePriceBase = (requests.get(ProductsEndpoint, auth=AppAuth, params=PriceParams))

# Use List Comprehension to morph the product list to a more manageable size.
# For more info on List Comprehension: https://www.w3schools.com/python/python_lists_comprehension.asp
for item in WebsitePriceList:
    [item.pop(key) for key in Filter_Products]

UpdateSource = json.loads(LocalPriceJSON)
UpdateTarget = WebsitePriceList

NextLink = requests.get(ProductsEndpoint, auth=AppAuth, params=PriceParams).links['next']['url']

# Product Update Addition Loop
while NextLink:
    UpdateTargetAddon = requests.get(NextLink, auth=AppAuth).json()
    for item in UpdateTargetAddon:
        [item.pop(key) for key in Filter_Products]
    UpdateTarget.extend(UpdateTargetAddon)
    try:
        if requests.get(NextLink, auth=AppAuth).links['next']['url']:
            print('Going to next page...')
            NextLink = requests.get(NextLink, auth=AppAuth).links['next']['url']
    except KeyError:
        print('Reached end of applicable products list. Moving on...')
        break
'''
while NextLink:
    UpdateTargetAddon = requests.get(NextLink, auth=AppAuth).json()
    for item in UpdateTargetAddon:
        [item.pop(key) for key in Filter_Products]
    UpdateTarget.extend(UpdateTargetAddon)
    while requests.get(NextLink, auth=AppAuth).links['next']['url']:
        NextLink = requests.get(NextLink, auth=AppAuth).links['next']['url']
'''