#!/usr/bin/env python3
"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
from flask import Blueprint, flash, g, redirect, render_template, request, Response, session, url_for, jsonify
from werkzeug.security import check_password_hash
from src.auth import login_required
from src.db import get_db
from src.dnacAPI import *
from src.primeAPI import *
from src.bmcAPI import *
from src.teamsBot import *
from datetime import datetime
import json
import urllib3
import pprint

urllib3.disable_warnings()
bp = Blueprint('portal', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def home():
    """
    Home Page back-end functionality
    :return:
    """
    error = None
    dnac_status = False
    prime_status = False
    bmc_status = False
    mksft_teams_status = False

    required_keys = ["dnac", "prime", "bmc", "mksft_teams"]
    for key in required_keys:
        if key not in session:
            return redirect(url_for('portal.settings'))

    dnac_status = session['dnac'].get('dnac_Token', "") != ""
    prime_status = session['prime'].get('prime_host', "") != ""
    bmc_status = session['bmc'].get('bmc_Token', "") != ""
    mksft_teams_status = session['mksft_teams'].get('webhook_url', "") != ""

    if error is not None:
        flash(error)

    return render_template('portal/home.html', dnac_status=dnac_status,
        prime_status=prime_status, bmc_status=bmc_status,
        mksft_teams_status=mksft_teams_status)


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    """
    Settings Page back-end functionality
    :return:
    """
    error = None
    dnac = {}
    prime = {}
    bmc = {}
    mksft_teams = {}

    if 'dnac' in session:
        dnac = session['dnac']
    if 'prime' in session:
        prime = session['prime']
    if 'bmc' in session:
        bmc = session['bmc']
    if 'mksft_teams' in session:
        mksft_teams = session['mksft_teams']

    if request.method == 'POST':
        # Check for any DNA-Center inputs
        if request.form.get('dnac_host') != "":
            dnac["dnac_host"] = request.form.get('dnac_host')
        if request.form.get('dnac_username') != "":
            dnac["dnac_username"] = request.form.get('dnac_username')
        if request.form.get('dnac_password') != "":
            dnac["dnac_password"] = request.form.get('dnac_password')
        session['dnac'] = dnac
        if 'dnac' in session and session['dnac'] != {}:
            session['dnac']['dnac_Token'] = get_Dna_Token(session['dnac'])

        # Check for any Prime inputs
        if request.form.get('prime_host') != "":
            prime["prime_host"] = request.form.get('prime_host')
        if request.form.get('prime_username') != "":
            prime["prime_username"] = request.form.get('prime_username')
        if request.form.get('prime_password') != "":
            prime["prime_password"] = request.form.get('prime_password')
        session['prime'] = prime

        # Check for any BMC inputs
        if request.form.get('bmc_host') != "":
            bmc["bmc_host"] = request.form.get('bmc_host')
        if request.form.get('bmc_username') != "":
            bmc["bmc_username"] = request.form.get('bmc_username')
        if request.form.get('bmc_password') != "":
            bmc["bmc_password"] = request.form.get('bmc_password')
        session['bmc'] = bmc
        if 'bmc' in session and session['bmc'] != {}:
            session['bmc']['bmc_Token'] = get_Bmc_Token(session['bmc'])

        # Check for any Microsoft Teams inputs
        if request.form.get('webhook_url') != "":
            mksft_teams['webhook_url'] = request.form.get('webhook_url')
        session['mksft_teams'] = mksft_teams

        return redirect(url_for('portal.home'))

    if error is not None:
        flash(error)
    return render_template('portal/settings.html', session=session)

@bp.route('/complete', methods=('GET', 'POST'))
@login_required
def portalComplete():
    session['dnac']['events'] = []
    session['prime']['alarms'] = []

    required_keys = ["dnac", "prime", "bmc", "mksft_teams"]
    for key in required_keys:
        if key not in session:
            return redirect(url_for('portal.settings'))

    dnac_status = session['dnac'].get('dnac_Token', "") != ""
    prime_status = session['prime'].get('prime_host', "") != ""
    bmc_status = session['bmc'].get('bmc_Token', "") != ""
    mksft_teams_status = session['mksft_teams'].get('webhook_url', "") != ""

    #session['dnac']['events'] = get_Dna_Events(session['dnac'])
    #session['prime']['alarms'] = get_Prime_Alarms(session['prime'])
    #create_Bmc_Incident_Dnac(session['bmc'], session['dnac']['events'])
    #create_Bmc_Incident_Prime(session['bmc'], session['prime']['alarms'])
    #send_Teams_Message_Dnac(session['mksft_teams']['webhook_url'], session['dnac']['events'])
    #send_Teams_Message_Prime(session['mksft_teams']['webhook_url'], session['prime']['alarms'])

    if 'events' in session['dnac'] or 'alarms' in session['prime']:
        return render_template('portal/complete.html', dnac_status=dnac_status,
                prime_status=prime_status, bmc_status=bmc_status,
                mksft_teams_status=mksft_teams_status,
                # dnac_events=session['dnac']['events'],
                # prime_alarms=session['prime']['alarms'])
                dnac_events=[],
                prime_alarms=[])

    return redirect(url_for('portal.home'))

@bp.route('/events', methods=('GET',))
@login_required
def events():
    session['dnac']['events'] = get_Dna_Events(session['dnac'])
    create_Bmc_Incident_Dnac(session['bmc'], session['dnac']['events'])
    send_Teams_Message_Dnac(session['mksft_teams']['webhook_url'], session['dnac']['events'])
    session['prime']['alarms'] = get_Prime_Alarms(session['prime'])
    pprint.pprint(session['prime']['alarms'])
    create_Bmc_Incident_Prime(session['bmc'], session['prime']['alarms'])
    send_Teams_Message_Prime(session['mksft_teams']['webhook_url'], session['prime']['alarms'])

    try:
        events = []
        for event in session['dnac']['events']:
            evt = {
                "id": event["eventId"],
                "name": event["name"],
                "description": event["description"],
                "type": "dnac",
            }
            events.append(evt)
        for alarm in session['prime']['alarms']:
            evt = {
                "id": alarm['queryResponse']['entity'][0]['alarmsDTO']['@id'],
                "name": alarm['queryResponse']['entity'][0]['alarmsDTO']['condition']['value'],
                "description": alarm['queryResponse']['entity'][0]['alarmsDTO']['message'],
                "type": "prime"
            }
            events.append(evt)
    except KeyError as e:
        print(str(e))


    return jsonify(events)
