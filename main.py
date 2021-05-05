import pandas as pd
import json
import requests
from requests import utils
from requests_oauthlib import OAuth1Session, OAuth1
from urllib.parse import urlencode
from woocommerce import API
import functions
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
Filter_Variations = config['ETL']['FilterPriceVar']
PriceParams = {'status': 'publish',
               'type': 'variable',
               'per_page': 50}

# Endpoints
AuthEndpoint = BaseURL + config['WC']['endpoints']['auth']
ProductsEndpoint = BaseURL + config['WC']['endpoints']['products']
OrdersEndpoint = BaseURL + config['WC']['endpoints']['orders']
CategoriesEndpoint = BaseURL + config['WC']['endpoints']['categories']
VarEndpointBase = config['WC']['endpoints']['variations']

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

# Local data from data.py
LocalPriceDF = data.df
LocalPriceJSON = LocalPriceDF.to_json(orient="records")

WebsitePriceList = (requests.get(ProductsEndpoint, auth=AppAuth, params=PriceParams).json())
WebsitePriceBase = (requests.get(ProductsEndpoint, auth=AppAuth, params=PriceParams))

UpdateSource = json.loads(LocalPriceJSON)
UpdateTarget = WebsitePriceList

NextLink = requests.get(ProductsEndpoint, auth=AppAuth, params=PriceParams).links['next']['url']

# Product Update Addition Loop
print('Retrieving list of update-able products from API')
print('adding page 1 to update-able products')
while NextLink:
    print('adding page '+NextLink[-1]+' to update-able products')
    UpdateTargetAddon = requests.get(NextLink, auth=AppAuth).json()
    UpdateTarget.extend(UpdateTargetAddon)
    print('Adding products from page...')
    try:
        if requests.get(NextLink, auth=AppAuth).links['next']['url']:
            print('Updating next page link...')
            NextLink = requests.get(NextLink, auth=AppAuth).links['next']['url']
    except KeyError:
        print('Reached end of applicable products list. Moving on...')
        break

print('trimming:')
print(Filter_Products)
print('from product page')
# Use List Comprehension to morph the product list to a more manageable size.
# For more info on List Comprehension: https://www.w3schools.com/python/python_lists_comprehension.asp
for item in UpdateTarget:
    [item.pop(key) for key in Filter_Products]

print('Completed UpdateTarget product list creation. Results:')
print('Update-able product list contains '+str(len(UpdateTarget))+' products')

# Grab IDs from product update list
for product in UpdateTarget:
    print((str(product['id'])) + ', ' + (product['name']) + ', ' + (product['price']))


# Creating workable list of variations and adding specific variation API endpoints
VarIDList = []
Variations = []
for Product in UpdateTarget:
    VarIDAdd = {'id' : Product['id'], 'variations' : []}
    for variable in Product['variations']:
        AddURL = {'var_id': variable, 'url' : ProductsEndpoint + str(Product['id']) + VarEndpointBase + str(variable)}
        VarIDAdd['variations'].append(AddURL)
    VarIDList.append(VarIDAdd)
    Variations.extend(Product['variations'])

# Call the API to get Variation info
# This takes a while. May be a more resource/time effective way to do this...?
FinalVarList = []
for ID in VarIDList:
    FinalVarAdd = {}
    for variation in ID['variations']:
        AddInfo = requests.get(variation['url'], auth=AppAuth, params=PriceParams).json()
        [AddInfo.pop(key) for key in Filter_Variations]
        print(AddInfo)
        FinalVarList.append(AddInfo)

# Create list of ItemIDs to grab from local DB
ItemIDList = []
for var in FinalVarList:
    add = var['sku']
    ItemIDList.append(add)

# Trim UpdateSource into only containing items we retrieved from WooCommerce
UpdateSource = functions.trim_sql_results(UpdateSource, ItemIDList)

# Next step is adding the website price to the update list

