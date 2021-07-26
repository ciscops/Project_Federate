#!/usr/bin/env python3
import requests

#check if the IP address or url is accessible

def checkIp(ip_addr):
    url = "https://{}".format(ip_addr)
    try:
        #try to send a HTTP GET request to provided url
        #if GET operation isn't complete after 5 seconds, quit trying
        response = requests.get(url, timeout=5, verify=False)
    except:
        #the GET operation failed
        return False

    if response.status_code == requests.codes.ok:
        #the GET operation returned an OK status code
        return True

    #the GET operation did not return an OK status code
    return False
