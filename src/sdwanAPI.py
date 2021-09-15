#!/usr/bin/env python3
import requests
import urllib3
import json

urllib3.disable_warnings()

class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host, username, password):
        api = "/j_security_check"
        base_url = "https://%s"%(vmanage_host)
        url = base_url + api
        payload = {'j_username' : username, 'j_password' : password}

        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return(jsessionid[0])
        except:
            print("No valid JSESSION ID returned\n")
            exit()

    @staticmethod
    def get_token(vmanage_host, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s"%(vmanage_host)
        api = "/dataservice/client/token"
        url = base_url + api      
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None

vmanage_host= 'sandbox-sdwan-1.cisco.com'
vmanage_username = 'devnetuser'
vmanage_password='RG!_Yw919_83'
vmanage_port='8443'
Auth = Authentication()
jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_username,vmanage_password)
token = Auth.get_token(vmanage_host,jsessionid)


if token is not None:
    header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json",'Cookie': jsessionid}

#API call to retrieve SDWAN events
def get_Sdwan_Events(dnac):
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
