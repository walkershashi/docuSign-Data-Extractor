# Import Libraries
import requests
from getFormData import getData
from refreshTokens import refresh
from configparser import ConfigParser

# Function to get the folder Ids
def getFolderId(acc_id, header):
    folderResponse = requests.get("https://demo.docusign.net/restapi/v2.1/accounts/{}/folders".format(acc_id), headers=header).json()

    folder_ids = []
    folders = folderResponse["folders"]

    for folder in folders:
        # Remove the unwanted folders
        if folder["type"] not in  ["recyclebin", "draft"]:
            folder_ids.append(folder["folderId"])

    return ",".join(folder_ids)

# Function to get the account Id
def getAccountId(header):
    userInfo = requests.get('https://account-d.docusign.com/oauth/userinfo', headers = header).json()

    return userInfo["accounts"][0]["account_id"]

# Get the tokens
config = ConfigParser()
config.read("tokens.ini")

tokens = config["Tokens"]
accessToken = tokens['access_token'] 

# Define header
header = {
    "Authorization": "Bearer " + accessToken
}

# Get Account ID
account_id = getAccountId(header)

# Get Folder ID
folder_ids = getFolderId(account_id, header)

# Get all envelopes in the folders
envelopeResponse = requests.get(
    "https://demo.docusign.net/restapi/v2.1/accounts/{}/envelopes?folder_ids={}".format(
        account_id,
        folder_ids
    ),
    headers = header
).json()

envelopes = envelopeResponse["envelopes"]

for envelope in envelopes:
    # Get the data for each envelope ID
    print("")
    print(envelope["envelopeId"])
    getData(account_id, envelope["envelopeId"])
    print("")

# Refresh the tokens
refresh()
