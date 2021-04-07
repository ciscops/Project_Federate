#!/usr/bin/env python3
import requests
import urllib3
import json

urllib3.disable_warnings()


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
	resp = requests.post(url, auth=(dnac['dnac_username'], dnac['dnac_password']),
        headers=headers, verify=False).json()

	# Validate Response
	if 'error' in resp:
		print('ERROR: Failed to retrieve Access Token!')
		print('REASON: {}'.format(resp['error']))
		result = ""
	else:
		result = resp['Token']

	return result


def get_Dna_Events(dnac):
    url = 'https://{}/dna/intent/api/v1/events?tags=ASSURANCE'
    headers = {
        'x-auth-token': get_Dna_Token(dnac),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    resp = requests.get(url, headers=headers, verify=False).json()

    if 'error' in resp:
        print('ERROR: Failed to retrieve events')
        print('REASON: {}'.format(resp['error']))
        result = ''
    else:
        result = resp

    return result
