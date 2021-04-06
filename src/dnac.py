#!/usr/bin/env python3
import requests
import json
import urllib3
import pymsteams
import pprint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#retrieve DNA Center API token
dnac_base_url = 'https://10.93.141.35/dna/'
dnac_auth_endpoint = 'system/api/v1/auth/token'
dnac_user = 'demotme'
dnac_password = 'apiuser123!'
dnac_auth_headers = {'Content-Type': 'application/json'}

dnac_auth = requests.post(url=dnac_base_url+dnac_auth_endpoint,
    auth=(dnac_user, dnac_password), headers=dnac_auth_headers,
    verify=False).json()
dnac_token = dnac_auth['Token']

#retrieve DNA Center Assurance events
events_endpoint = 'intent/api/v1/events?tags=ASSURANCE'
events_headers = {
    'x-auth-token': dnac_token,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

events_response = requests.get(url=dnac_base_url+events_endpoint, headers=events_headers,
    verify=False).json()

#send event information to Microsoft Teams
myTeamsMessage = pymsteams.connectorcard("https://yasgari.webhook.office.com/webhookb2/2755b1ee-5bef-4118-b3dc-5dbdffb32957@b64e9a93-20fd-4ff3-912f-b107db4df8a6/IncomingWebhook/214b7ec7934046ccb3c7d976c546857a/61e30099-b8ed-4ac8-b43d-5f3d26825dc5")

for event in events_response:
    #TODO: figure out details of what to send in Teams message
    myTeamsMessage.text(event['name'] + ': ' + event['description'])
    myTeamsMessage.send()

#retrieve Remedy API token
remedy_base_url = 'http://{SERVER NAME}:{PORT}/'
remedy_auth_endpoint = 'api/jwt/login'
remedy_user = 'user'
remedy_password = 'password'
remedy_auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

remedy_token = requests.post(url=remedy_base_url+remedy_auth_endpoint,
    auth=(remedy_user, remedy_password), headers=remedy_auth_headers,
    verify=False)

#create Remedy incident with DNA Center Assurance event info
incident_endpoint = 'api/arsys/v1/entry/HPD:IncidentInterface_Create?fields=values(Incident Number)'
incident_headers = {
    'Authorization': 'AR-JWT' + remedy_token,
    'Content-Type': 'application/json'
    }
incident_body = {
    'values': {
        'First_Name': #TODO: find value for key,
        'Last_Name':#TODO: find value for key,
        'Description': events_response['description'],
        'Impact': #TODO: find value for key,
        'Urgency': events_response['severity'],
        'Status': #TODO: find value for key,
        'Reported Source': #TODO: find value for key,
        'Service_Type': #TODO: find value for key
     }
    }

create_incident_response = requests.post(url=remedy_base_url+incident_endpoint,
    headers=incident_headers, data=incident_body, verify=False)
