# Import Libraries
import csv
import requests
from base64 import b64encode
from configparser import ConfigParser

# Function to refresh the tokens
def refresh():
    config = ConfigParser()
    config.read("tokens.ini")

    # Get previous tokens for exchange
    tokens = config["Tokens"]

    # Define Headers
    header = {
        "Authorization": "Basic " + "b64encode{Client_Id:Client_Secret}", # Base64 encoded
    }

    # Define Body
    body = {
        "grant_type": "refresh_token",
        "refresh_token": tokens['refresh_token']
    }

    response = requests.post('https://account-d.docusign.com/oauth/token', headers = header, data = body).json()

    # Store the new set of tokens in config file
    config.set("Tokens", "access_token", response['access_token'])
    config.set("Tokens", "refresh_token", response['refresh_token'])

    with open('tokens.ini', 'w') as configfile:
        config.write(configfile)

    print("tokens refreshed")