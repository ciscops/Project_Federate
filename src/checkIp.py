#!/usr/bin/env python3
import sys
import nmap, socket

#check if the IP address or url is accessible
def checkIp(ip_addr):
    scanner = nmap.PortScanner()

    try:
        host = socket.gethostbyname(ip_addr)
        scanner.scan(host, '1', '-v')

        if scanner[host].state() == 'up':
            return True

        return False

    except:
        e = sys.exc_info()[0]
        print("Error: ", str(e))

        return False
