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


def get_Epnm_Events(epnm):
    #retrieve epnm events with epnm api
    base_uri = 'https://' + epnm['epnm_host']
    user = epnm['epnm_username']
    password = epnm['epnm_password']
    #depending on amount of events in your environment, you may need to use pagination to retrieve results
    rest_path = '/webacs/api/v4/data/Events.json?.full=true&.maxResults=20&.firstResult=80'
    # rest_path = '/webacs/api/v4/data/Events.json'

    url = base_uri + rest_path
    response = requests.get(url, auth=(user, password), verify=False)
    response = json.loads(response.content)
    events = response['queryResponse']['entity']

    event_list = []

    for event in events:
        #epnm returns the url to make api calls to retrieve information about specific events
        url = event['@url'] + '.json'
        response = requests.get(url, auth=(user, password), verify=False)

        event_list.append(response.json())
    print("Event LIST EPNM", event_list)
    return event_list
