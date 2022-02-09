#!/usr/bin/env python3
import requests
import urllib3
import json

urllib3.disable_warnings()


#Retrieve DNAC token to use for DNAC API calls
def get_Dna_Token(dnac):
    """
    Intent-based Authentication API call
    The token obtained using this API is required to be set as value to the X-Auth-Token HTTP Header
    for all API calls to Cisco DNA Center.
    :param: dnac
    :return: Token STRING
    """
    url = 'https://{}/dna/system/api/v1/auth/token'.format(dnac['dnac_host'])
    headers = {'Content-Type': 'application/json'}
    # Make the POST Request
    resp = requests.post(url, auth=(dnac['dnac_username'], dnac['dnac_password']), headers=headers, verify=False)

    # Validate Response
    if 'error' in resp.json():
        print('ERROR: Failed to retrieve Access Token!')
        print('REASON: {}'.format(resp.json()['error']))
        result = ""
    else:
        result = resp.json()['Token']

    return result


#API call to retrieve DNAC events
def get_Dna_Events(dnac):
    url = 'https://{}/dna/intent/api/v1/events?tags=ASSURANCE'.format(dnac['dnac_host'])
    headers = {
        'x-auth-token': dnac['dnac_Token'],
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    resp = requests.get(url, headers=headers, verify=False)

    if 'error' in resp.json():
        print('ERROR: Failed to retrieve DNAC events')
        print('REASON: {}'.format(resp.json()['error']))
        result = ""
    elif 'exp' in resp.json():
        print('ERROR: Failed to retrieve DNAC events')
        print('REASON: {}'.format(resp.json()['exp']))
        result = ""
    else:
        result = resp.json()

    return result


def get_Dna_Health(dnac):
    url = 'https://{}/dna/intent/api/v1/network-health'.format(dnac['dnac_host'])
    headers = {
        'x-auth-token': dnac['dnac_Token'],
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    resp = requests.get(url, headers=headers, verify=False)
    print('response from DNAC health ', resp.json()['response'][0]['healthScore'])
    return resp.json()['response'][0]['healthScore']