#!/usr/bin/env python3
# import sys
# import nmap, socket
# import os
import requests

#check if the IP address or url is accessible
'''def checkIp(ip_addr):
    scanner = nmap.PortScanner()
    host = socket.gethostbyname(ip_addr)

    try:
        scanner.scan(host, '1', '-v')
    except:
        e = sys.exc_info()[0]
        print("Error: ", str(e))

        return False


    if scanner[host].state() == 'up':
        return True

    return False'''

def checkIp(ip_addr):
    url = "https://{}".format(ip_addr)
    try:
        response = requests.get(url, timeout=5, verify=False)
    except:
        return False

    if response.status_code == requests.codes.ok:
        return True

    return False
