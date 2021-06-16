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
from src.checkIp import checkIp
from datetime import datetime
import json
import urllib3
import pprint
import threading
import queue

urllib3.disable_warnings()

q = queue.Queue()
def do_queue():
    global q
    while True:
        job = q.get()
        job()
        q.task_done()

consumer = threading.Thread(target=do_queue)
consumer.daemon = True
consumer.start()

try:
    bp = Blueprint('portal', __name__)
except KeyboardInterrupt:
    q.join()


@bp.route('/', methods=('GET', 'POST'))
@login_required
def home():
    required_keys = ["dnac", "prime", "bmc", "mksft_teams"]
    for key in required_keys:
        if key not in session:
            return redirect(url_for('portal.settings'))

    dnac = session["dnac"]
    prime = session["prime"]
    dnac["events"] = []
    prime["events"] = []
    session["dnac"] = dnac
    session["prime"] = prime

    dnac_status = checkIp(session["dnac"]["dnac_host"])
    prime_status = checkIp(session["prime"]["prime_host"])
    bmc_status = checkIp(session["bmc"]["bmc_host"])
    # mksft_teams_status = checkConnection(session["mksft_teams"]["webhook_url"])
    # dnac_status = session['dnac'].get('dnac_Token', "") != ""
    # prime_status = session['prime'].get('prime_host', "") != ""
    # bmc_status = session['bmc'].get('bmc_Token', "") != ""
    mksft_teams_status = session['mksft_teams'].get('webhook_url', "") != ""

    if 'events' in session['dnac'] or 'events' in session['prime']:
        return render_template('portal/home.html', dnac_status=dnac_status,
                prime_status=prime_status, bmc_status=bmc_status,
                mksft_teams_status=mksft_teams_status,
                dnac_events=[],
                prime_events=[])

    return redirect(url_for('portal.home'))


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
        session["dnac"] = dnac
        if 'dnac' in session and session['dnac'] != {}:
            dnac_token = get_Dna_Token(dnac)
            dnac["dnac_Token"] = dnac_token
            session["dnac"] = dnac

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
            bmc_token = get_Bmc_Token(bmc)
            bmc["bmc_Token"] = bmc_token
            session["bmc"] = bmc

        # Check for any Microsoft Teams inputs
        if request.form.get('webhook_url') != "":
            mksft_teams['webhook_url'] = request.form.get('webhook_url')
        session['mksft_teams'] = mksft_teams

        return redirect(url_for('portal.home'))

    if error is not None:
        flash(error)
    return render_template('portal/settings.html', session=session)


@bp.route('/dnacLogs', methods=('GET',))
@login_required
def dnacLogs():
    dnac_events = session["dnac"]["events"]
    return render_template('portal/dnacLogs.html', dnac_events=dnac_events)


@bp.route('/primeLogs', methods=('GET',))
@login_required
def primeLogs():
    prime_events = session["prime"]["events"]
    return render_template('portal/primeLogs.html', prime_events=prime_events)


@bp.route('/events', methods=('GET',))
@login_required
def events():
    dnac = session['dnac']
    prime = session['prime']
    dnac['events'] = get_Dna_Events(session['dnac'])
    prime['events'] = get_Prime_Events(session['prime'])
    dnac_events = []
    prime_events = []
    for dnac_event in dnac["events"]:
        dnac_evt = {
            "id": dnac_event["eventId"],
            "name": dnac_event["name"],
            "description": dnac_event["description"],
            "severity": dnac_event["severity"],
            "type": "dnac"
        }
        dnac_events.append(dnac_evt)
    for prime_event in prime["events"]:
        prime_evt = {
            "id": prime_event['queryResponse']['entity'][0]['eventsDTO']['@id'],
            "name": prime_event['queryResponse']['entity'][0]['eventsDTO']['condition']['value'],
            "description": prime_event['queryResponse']['entity'][0]['eventsDTO']['description'],
            "severity": prime_event['queryResponse']['entity'][0]['eventsDTO']['severity'],
            "type": "prime"
        }
        prime_events.append(prime_evt)

    dnac["events"] = dnac_events
    prime["events"] = prime_events
    session['dnac'] = dnac
    session['prime'] = prime
    bmc = session['bmc']
    teams_url = session['mksft_teams']['webhook_url']
    session.modified = True

    q.put(lambda: create_Bmc_Incident_Dnac(bmc, dnac_events))
    q.put(lambda: create_Bmc_Incident_Prime(bmc, prime_events))
    q.put(lambda: send_Teams_Message_Dnac(teams_url, dnac_events))
    q.put(lambda: send_Teams_Message_Prime(teams_url, prime_events))

    events = dnac_events + prime_events

    '''try:
        events = []
        for dnac_event in session['dnac']['events']:
            evt = {
                "id": dnac_event["id"],
                "name": dnac_event["name"],
                "description": dnac_event["description"],
                "type": "dnac"
            }
            events.append(evt)
        for prime_event in session['prime']['events']:
            evt = {
                "id": prime_event['queryResponse']['entity'][0]['eventsDTO']['@id'],
                "name": prime_event['queryResponse']['entity'][0]['eventsDTO']['condition']['value'],
                "description": prime_event['queryResponse']['entity'][0]['eventsDTO']['description'],
                "type": "prime"
            }
            events.append(evt)
    except KeyError as e:
        print(str(e))'''

    return jsonify(events)
