#!/usr/bin/env python3
import requests
import urllib3
import json

def get_Bmc_Token(bmc):
    url = 'http://{}/api/jwt/login'.format(bmc['bmc_host'])
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # resp = requests.post(url, auth=(bmc['bmc_username'], bmc['bmc_password']),
        # headers=headers, verify=False)

    #Validate response
    '''if 'error' in resp.json():
        print('ERROR: Failed to retrieve Access Token!')
        print('REASON: {}'.format(resp.json()['error']))

        result = ''
    else:
        result = resp.json()['Token']'''

    print('BMC token API call: \n URL: {} \n Headers: {} \n Authorization: {}'.format(url, headers, (bmc['bmc_username'], bmc['bmc_password'])))
    result = 'TOKEN GOES HERE'
    return result

def create_Bmc_incident(bmc, events):
    url = 'http://{}/api/arsys/v1/entry/HPD:IncidentInterface_Create?fields=values(Incident Number)'.format(bmc['bmc_host'])
    headers = {
        'Authorization': 'AR-JWT ' + bmc['bmc_Token'],
        'Content-Type': 'application/json'
        }
    for event in events:
        body = {
            'values': {
                'First_Name': 'John',
                'Last_Name': 'Smith',
                'Description': event['description'],
                'Impact': 'Big',
                'Urgency': event['severity'],
                'Status': 'Unknown',
                'Reported Source': 'ME',
                'Service_Type': 'Probably switch'
            }
        }
        # resp = requests.post(url, headers=headers, data=body, verify=False)
        print('BMC incident API call: \n URL: {} \n Headers: {} \n Body: {}'.format(url, headers, body))
