#!/usr/bin/env python3
import pymsteams

def send_Teams_Message_Dnac(mksft_teams, events):
    myTeamsMessage = pymsteams.connectorcard(mksft_teams)

    for event in events:
        myTeamsMessage.text('DNAC Event: ' + event['name'] + ': ' + event['description'])
        myTeamsMessage.send()


def send_Teams_Message_Prime(mksft_teams, events):
    myTeamsMessage = pymsteams.connectorcard(mksft_teams)

    for event in events:
        event_name = event['name']
        event_description = event['description']

        myTeamsMessage.text('Prime Event: ' + event_name + ': ' + event_description)
        myTeamsMessage.send()


def checkConnection(mksft_teams):
    myTeamsMessage = pymsteams.connectorcard(mksft_teams)
    myTeamsMessage.text('Incoming Events Notifications...')
    myTeamsMessage.send()

    status_code = myTeamsMessage.last_http_status.status_code

    if status_code == 200:
        return True

    return False
