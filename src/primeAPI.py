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

def get_Prime_Events(prime):
    base_uri = prime['prime_host']
    user = prime['prime_username']
    password = prime['prime_password']
    rest_path = '/webacs/api/v4/data/Events.json?.full=true&.maxResults=20&.firstResult=80'
    # rest_path = '/webacs/api/v4/data/Events.json'

    url = base_uri + rest_path
    response = requests.get(url, auth=(user, password), verify=False)
    response = json.loads(response.content)
    events = response['queryResponse']['entity']

    event_list = []

    for event in events:
        url = event['@url'] + '.json'
        response = requests.get(url, auth=(user, password), verify=False)

        event_list.append(response.json())

    return event_list
