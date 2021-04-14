#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json
import pprint

##########
# SET-UP #
##########
urllib3.disable_warnings()

#############
# FUNCTIONS #
#############

def get_Prime_Alarms(prime):
    base_uri = prime['prime_host']
    user = prime['prime_username']
    password = prime['prime_password']
    rest_path = '/webacs/api/v4/data/Alarms.json'

    url = base_uri + rest_path
    response = requests.get(url, auth=(user, password), verify=False)
    alarms = response.json()['queryResponse']['entityId']

    alarm_list = []

    for alarm in alarms:
        url = alarm['@url'] + '.json'
        response = requests.get(url, auth=(user, password), verify=False)

        alarm_list.append(response.json())

    return alarm_list
