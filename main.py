#
import pandas as pd
import requests
import yaml

# Retrieve config info and set variables
with open("config.yml", 'r') as config:
    yamlInfo = yaml.safe_load(config)
apiKey = yamlInfo['WooCommerce']['apiKey']
apiSecret = yamlInfo['WooCommerce']['apiSecret']
baseURL = yamlInfo['WooCommerce']['baseURL']
