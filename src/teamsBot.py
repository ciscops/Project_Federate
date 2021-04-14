#!/usr/bin/env python3
import pymsteams

def send_Teams_Message_Dnac(mksft_teams, events):
    myTeamsMessage = pymsteams.connectorcard(mksft_teams)

    for event in events:
        myTeamsMessage.text('DNAC Event         ' + event['name'] + ': ' + event['description'])
        myTeamsMessage.send()


def send_Teams_Message_Prime(mksft_teams, alarms):
    myTeamsMessage = pymsteams.connectorcard(mksft_teams)

    for alarm in alarms:
        alarm_name = alarm['queryResponse']['entity'][0]['alarmsDTO']['condition']['value']
        alarm_description = alarm['queryResponse']['entity'][0]['alarmsDTO']['message']

        myTeamsMessage.text('Prime Alarm        ' + alarm_name + ': ' + alarm_description)
        myTeamsMessage.send()
