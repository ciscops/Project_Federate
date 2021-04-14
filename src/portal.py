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
from flask import Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
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

    dnac_events = []
    prime_alarms = []

    if 'dnac' in session:
        session['dnac']['dnac_Token'] = get_Dna_Token(session['dnac'])

        if session['dnac']['dnac_Token'] != "":
            dnac_status = True

        dnac_events = get_Dna_Events(session['dnac'])
    else:
        return redirect(url_for('portal.settings'))

    if 'prime' in session:
        if session['prime']['prime_host'] != "":
            prime_status = True

        prime_alarms = get_Prime_Alarms(session['prime'])

    else:
        return redirect(url_for('portal.settings'))

    if 'bmc' in session:
        session['bmc']['bmc_Token'] = get_Bmc_Token(session['bmc'])

        if session['bmc']['bmc_Token'] != "":
            bmc_status = True

        create_Bmc_Incident_Dnac(session['bmc'], dnac_events)
        create_Bmc_Incident_Prime(session['bmc'], prime_alarms)
    else:
        return redirect(url_for('portal.settings'))

    if 'mksft_teams' in session:
        if session['mksft_teams']['webhook_url'] != "":
            mksft_teams_status = True

        send_Teams_Message_Dnac(session['mksft_teams']['webhook_url'], dnac_events)
        send_Teams_Message_Prime(session['mksft_teams']['webhook_url'], prime_alarms)
    else:
        return redirect(url_for('portal.settings'))

    if error is not None:
        flash(error)

    return render_template('portal/home.html', dnac_status=dnac_status,
        prime_status=prime_status, bmc_status=bmc_status,
        mksft_teams_status=mksft_teams_status, dnac_events=dnac_events,
        prime_alarms=prime_alarms)


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

        # Check for any Microsoft Teams inputs
        if request.form.get('webhook_url') != "":
            mksft_teams['webhook_url'] = request.form.get('webhook_url')
        session['mksft_teams'] = mksft_teams

        return redirect(url_for('portal.home'))

    if error is not None:
        flash(error)
    return render_template('portal/settings.html', session=session)
