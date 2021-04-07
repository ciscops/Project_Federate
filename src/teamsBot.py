#!/usr/bin/env python3
import pymsteams

def send_Teams_Message(mksft_teams, events):
    myTeamsMessage = pymsteams.connectorcard(mksft_teams)

    for event in events:
        myTeamsMessage.text('''TODO: figure out which details to send''')
        myTeamsMessage.send()
