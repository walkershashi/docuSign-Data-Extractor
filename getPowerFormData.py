# Import Libraries
import requests
from insertSQL import insert
from refreshTokens import refresh
from configparser import ConfigParser

# Get account id
def getAccountId(header):
    userInfo = requests.get('https://account-d.docusign.com/oauth/userinfo', headers = header).json()

    return userInfo["accounts"][0]["account_id"]

# Function to get the power form Id
def getPowerFormId(acc_id, header):
    powerFormResponse = requests.get("https://demo.docusign.net/restapi/v2.1/accounts/{}/powerforms".format(acc_id), headers=header).json()

    powerform_ids = []
    powerforms = powerFormResponse["powerForms"]

    for powerform in powerforms:
        powerform_ids.append(powerform["powerFormId"])
    
    return powerform_ids

# Function to get the power form data
def getPowerFormData(account_id, powerformId, header):
    powerFormData = requests.get("https://demo.docusign.net/restapi/v2.1/accounts/{}/powerforms/{}/form_data".format(
        account_id,
        powerformId
    ), headers = header).json()

    try:
        for envelopes in powerFormData["envelopes"]:
            envelopeId = envelopes["envelopeId"] # Get envelope ID
            for formData in envelopes["recipients"]:
                # Define SQL columns
                sql_cols = ["envelopeId", "powerformId"]
                sql_rows = [envelopeId, powerformId]
                data = []

                try:
                    data = formData["formData"]
                    for pairs in data:
                        if "Text" in pairs["name"]:
                            sql_cols.append("Text")
                            sql_rows.append(pairs["value"])
                        elif "Checkbox" in pairs["name"]:
                            sql_cols.append("Checkbox")
                            sql_rows.append(pairs["value"])
                        else:
                            sql_cols.append(pairs["name"])
                            sql_rows.append(pairs["value"])
                    
                    # Insert the data in SQL DB 
                    print("")
                    if len(sql_cols) == 2:
                        pass
                    else:
                        insert("powerFormData", sql_cols, sql_rows)
                    print("")
                    
                except:
                    pass
    except:
        pass

# Get the access token
config = ConfigParser()
config.read("tokens.ini")

tokens = config["Tokens"]
accessToken = tokens['access_token'] 

# Define headers
header = {
    "Authorization": "Bearer " + accessToken,
    "Accept": "application/json"
}

# Get IDs
account_id = getAccountId(header)
powerformIds = getPowerFormId(account_id, header)

# Get the powerform data
for powerform_id in powerformIds:
    getPowerFormData(account_id, powerform_id, header)

# Refresh the tokens
refresh()
