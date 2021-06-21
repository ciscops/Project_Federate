#!/usr/bin/env python3
import pymsteams

#send teams message about dnac events
def send_Teams_Message_Dnac(mksft_teams, events):
    myTeamsMessage = pymsteams.connectorcard(mksft_teams)

    for event in events:
        myTeamsMessage.text('DNAC Event: ' + event['name'] + ': ' + event['description'])
        myTeamsMessage.send()


#send teams message about prime events <- i think I can combine this into the above function
def send_Teams_Message_Prime(mksft_teams, events):
    myTeamsMessage = pymsteams.connectorcard(mksft_teams)

    for event in events:
        event_name = event['name']
        event_description = event['description']

        myTeamsMessage.text('Prime Event: ' + event_name + ': ' + event_description)
        myTeamsMessage.send()


#to get status of microsoft teams channel
def checkConnection(mksft_teams):
    '''send a message to the channel, and if the message is
    successfully sent, it will return a status code of 200.
    This indicates that the connection to the teams channel
    is up and running. Otherwise, the connection might not
    be up'''
    myTeamsMessage = pymsteams.connectorcard(mksft_teams)
    myTeamsMessage.text('Incoming Events Notifications...')
    myTeamsMessage.send()

    status_code = myTeamsMessage.last_http_status.status_code

    if status_code == 200:
        return True

    return False
