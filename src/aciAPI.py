#!/usr/bin/env python3
import requests
import urllib3
import json

urllib3.disable_warnings()


#Retrieve ACI token to use for ACI API calls
def get_Aci_Token(aci):
    """
    Intent-based Authentication API call
    The token obtained using this API is required to be set as value to the X-Auth-Token HTTP Header
    for all API calls to Cisco DNA Center.
    :param: aci
    :return: Token STRING
    """
    url = 'https://{}/api/v1/auth/login'.format(aci['aci_host'])
    headers = {'Content-Type': 'application/json'}
    # Make the POST Request
    resp = requests.post(url, auth=(aci['aci_username'], aci['aci_password']), headers=headers, verify=False)

    # Validate Response
    if 'error' in resp.json():
        print('ERROR: Failed to retrieve Access Token!')
        print('REASON: {}'.format(resp.json()['error']))
        result = ""
    else:
        result = resp.json()['token']

    return result


#API call to retrieve aci events
def get_Aci_Events(aci):
    url = 'https://{}/dna/intent/api/v1/events?tags=ASSURANCE'.format(aci['aci_host'])
    headers = {
        'x-auth-token': aci['aci_Token'],
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    resp = requests.get(url, headers=headers, verify=False)

    if 'error' in resp.json():
        print('ERROR: Failed to retrieve aci events')
        print('REASON: {}'.format(resp.json()['error']))
        result = ""
    elif 'exp' in resp.json():
        print('ERROR: Failed to retrieve aci events')
        print('REASON: {}'.format(resp.json()['exp']))
        result = ""
    else:
        result = resp.json()

    return result
