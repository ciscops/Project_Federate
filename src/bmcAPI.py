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

    print('BMC token API call: \n URL: {} \n Headers: {} \n Authorization: {}\n\n'.format(url, headers, (bmc['bmc_username'], bmc['bmc_password'])))
    result = 'TOKEN GOES HERE'
    return result

def create_Bmc_Incident_Dnac(bmc, events):
    url = 'http://{}/api/arsys/v1/entry/HPD:IncidentInterface_Create?fields=values(Incident Number)'.format(bmc['bmc_host'])
    headers = {
        'Authorization': 'AR-JWT ' + bmc['bmc_Token'],
        'Content-Type': 'application/json'
        }
    for event in events:
        severity = event['severity']
        if severity == 1:
            body = {
                'values': {
                    'First_Name': 'First Name Here',
                    'Last_Name': 'Last Name Here',
                    'Description': event['description'],
                    'Impact': 'Impact Here',
                    'Urgency': severity,
                    'Status': 'Status Here',
                    'Reported Source': 'Source Here',
                    'Service_Type': 'Service Type Here'
            }
        }
            # resp = requests.post(url, headers=headers, data=body, verify=False)
            print('BMC incident API call with DNAC event: \n URL: {} \n Headers: {} \n Body: {} \n\n'.format(url, headers, body))

def create_Bmc_Incident_Prime(bmc, events):
    url = 'http://{}/api/arsys/v1/entry/HPD:IncidentInterface_Create?fields=values(Incident Number)'.format(bmc['bmc_host'])
    headers = {
        'Authorization': 'AR-JWT ' + bmc['bmc_Token'],
        'Content-Type': 'application/json'
        }
    for event in events:
        severity = event['severity']
        if severity == 'CRITICAL' or severity == 'MAJOR':
            body = {
                'values': {
                    'First_Name': 'First Name Here',
                    'Last_Name': 'Last Name Here',
                    'Description': event['description'],
                    'Impact': 'Impact Here',
                    'Urgency': severity,
                    'Status': 'Status Here',
                    'Reported Source': 'Source Here',
                    'Service_Type': 'Service Type Here'
                    }
                }

            print('BMC incident API call with Prime event: \n URL: {} \n Headers: {} \n Body: {} \n\n'.format(url, headers, body))
