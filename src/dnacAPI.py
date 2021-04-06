from requests.auth import HTTPBasicAuth
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
	# Make the POST Request
	resp = requests.post(url, auth=HTTPBasicAuth(dnac['dnac_username'], dnac['dnac_password']), verify=False)

	# Validate Response
	if 'error' in resp.json():
		print('ERROR: Failed to retrieve Access Token!')
		print('REASON: {}'.format(resp.json()['error']))
		result = ""
	else:
		result = resp.json()['Token']
	return result