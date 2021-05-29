# Import Libraries
import csv
import requests
from base64 import b64encode
from configparser import ConfigParser

# Define Headers
header = {
    "Authorization": "Basic " + "b64encode{Client_Id:Client_Secret}", # Base64 encoded
}

# Define Body
body = {
    "grant_type": "authorization_code",
    "code": "{Code returned from the AuthURL}"
}
    
# Exchange the auth code for the access token and refresh token
response = requests.post('https://account-d.docusign.com/oauth/token', headers = header, data = body).json()

# Store the tokens in config file
config = ConfigParser()

if not config.has_section("Tokens"):
    config.add_section("Tokens")
    config.set("Tokens", "access_token", response['access_token'])
    config.set("Tokens", "refresh_token", response['refresh_token'])

else:
    config.set("Tokens", "access_token", response['access_token'])
    config.set("Tokens", "refresh_token", response['refresh_token'])

# Write config to a file
with open('tokens.ini', 'w') as configfile:
    config.write(configfile)
