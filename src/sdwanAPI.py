#!/usr/bin/env python3
import requests
import urllib3
import json

urllib3.disable_warnings()


class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host, vmanage_port, username, password):
        api = "/j_security_check"
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
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
    def get_token(vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api = "/dataservice/client/token"
        url = base_url + api      
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None


def authSDWAN(sdwan):
    Auth = Authentication()
    jsessionid = Auth.get_jsessionid(sdwan['sdwan_host'],443,sdwan['sdwan_username'],sdwan['sdwan_password'])
    token = Auth.get_token(sdwan['sdwan_host'],443,jsessionid)

    if token is not None:
        header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        header = {'Content-Type': "application/json",'Cookie': jsessionid}

    return header



#API call to retrieve sdwan events
def get_Sdwan_Events(sdwan):
    
    #Get critical events from the previous three hours
    query = {
        "query": {
            "condition": "AND",
            "rules": [
            {
                "value": [
                "100"
                ],
                "field": "entry_time",
                "type": "date",
                "operator": "last_n_hours"
            },
            {
                "value": [
                "critical"
                ],
                "field": "severity_level",
                "type": "string",
                "operator": "in"
            }
            ]
        }
    }

    url = 'https://'+sdwan['sdwan_host']+'/dataservice/event?query='+json.dumps(query)
    #url ='https://'+sdwan['sdwan_host']+'/dataservice/event'

    resp = requests.get(url, headers=sdwan["header"], verify=False)

    if 'error' in resp.json():
        print('ERROR: Failed to retrieve sdwan events')
        print('REASON: {}'.format(resp.json()['error']))
        result = ""
    elif 'exp' in resp.json():
        print('ERROR: Failed to retrieve sdwan events')
        print('REASON: {}'.format(resp.json()['exp']))
        result = ""
    else:
        result = resp.json()

    return result

