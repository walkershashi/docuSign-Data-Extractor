# Import Libraries
import json
import requests
from insertSQL import insert
from refreshTokens import refresh
from configparser import ConfigParser

# Function to extract the data from a single envelope using envelopeId
def getData(accountId, envId):
    # Get the access token
    config = ConfigParser()
    config.read("tokens.ini")
    
    tokens = config["Tokens"]

    accessToken = tokens['access_token']
    
    # Define header
    header = {
        "Authorization": "Bearer " + accessToken
    }

    account_id = accountId
    envelope_id =  envId

    # Get the formData response
    formData = requests.get(
        "https://demo.docusign.net/restapi/v2.1/accounts/{}/envelopes/{}/form_data".format(
            account_id,
            envelope_id
        ),
        headers = header
    ).json()

    form_data = ''
    
    # Check if data exists or not
    if formData['recipientFormData'] is None or len(formData['recipientFormData']) == 0:
        pass
    else:
        form_data = formData['recipientFormData']
    
        for data in form_data:
            recipient_data = data['formData']
            
            # Define SQL columns
            sql_cols = ['envelopeId']
            sql_data = [envelope_id]
            for recipient_data_i in recipient_data:
                
                if 'Name' in recipient_data_i["name"]:
                    if recipient_data_i["name"].split(" ")[0] != "Name":
                        sql_cols.append(recipient_data_i["name"].split(" ")[0] + "Name")
                    else:
                        sql_cols.append(recipient_data_i["name"].split(" ")[0])

                    sql_data.append(recipient_data_i["value"])
                
                if 'Email' in recipient_data_i["name"] or 'Email Address' in recipient_data_i["name"]:
                    sql_cols.append('EmailAddress')
                    sql_data.append(recipient_data_i["value"])
                
                if 'Text' in recipient_data_i["name"]:
                    sql_cols.append('Text')
                    sql_data.append(recipient_data_i["value"].replace("'", "_"))

                if 'Note' in recipient_data_i["name"]:
                    sql_cols.append('Note')
                    sql_data.append(recipient_data_i["value"].replace("'", "_"))
                
                if 'Title' in recipient_data_i["name"]:
                    sql_cols.append('Title')
                    sql_data.append(recipient_data_i["value"])

                if 'Company' in recipient_data_i["name"]:
                    sql_cols.append('Company')
                    sql_data.append(recipient_data_i["value"])
                
                if 'Checkbox' in recipient_data_i["name"]:
                    sql_cols.append("Checkbox")
                    sql_data.append(recipient_data_i["value"])
                
                if 'Date' in recipient_data_i["name"]:
                    sql_cols.append("DateSigned")
                    sql_data.append(recipient_data_i["value"])
            
            print(sql_cols)
            print(sql_data)
            print('')
            # Insert the Data in SQL DB
            insert("envelopeData", sql_cols, sql_data)
            print('')
            #return form_data

#getData()