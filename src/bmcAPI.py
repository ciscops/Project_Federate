#!/usr/bin/env python3
import requests
import urllib3
import json

def get_Bmc_Token(bmc):
    url = 'http://{}/api/jwt/login'.format(bmc['bmc_host'])
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    resp = requests.post(url, auth=(bmc['bmc_username'], bmc['bmc_password']),
        headers=headers, verify=False)

    #Validate response
    if 'error' in resp.json():
        print('ERROR: Failed to retrieve Access Token!')
        print('REASON: {}'.format(resp.json()['error']))

        result = ''
    else:
        result = resp.json()['Token']

    return result

def create_Bmc_incident(bmc, event):
    url = 'http://{}/api/arsys/v1/entry/HPD:IncidentInterface_Create?fields=values(Incident Number)'.format(bmc['bmc_host'])
    headers = {
        'Authorization': 'AR-JWT' + get_Bmc_Token(bmc),
        'Content-Type': 'application/json'
        }
    body = {
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

    resp = requests.post(url, headers=headers, data=body, verify=False)
