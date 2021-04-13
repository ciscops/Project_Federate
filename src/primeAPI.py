#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json

##########
# SET-UP #
##########
urllib3.disable_warnings()

#############
# FUNCTIONS #
#############
def prime_Get_Devices(env):
	url = "https://{}/webacs/api/v3/data/Devices".format(env['prime_base_url'])
	response = requests.request("GET", url, auth=HTTPBasicAuth(env['prime_username'], env['prime_password']), verify=False)
	print(response)


def prime_test_Function():
	base_uri = 'https://10.122.92.5/webacs/api/v4'
	user = 'yasgari'
	password = 'cisco123'
	rest_path = '/data/InventoryDetails'

	url = base_uri + rest_path
	response = requests.request('GET', url, auth=(user, password), verify=False)
	print(response.text)


prime_test_Function()
