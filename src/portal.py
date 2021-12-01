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
from src.epnmAPI import *
from src.bmcAPI import *
from src.aciAPI import *
from src.teamsBot import *
from src.checkIp import checkIp
from datetime import datetime
import json
import urllib3
import threading
import queue


urllib3.disable_warnings()

#need queue for multiprocessing the different API calls
q = queue.Queue()
def do_queue():
    global q
    while True:
        job = q.get()
        try:
            job()
        except Exception as e:
            print("Failed a job")
            print(str(e))
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
    '''the home page will display the statuses of dnac, prime, epnm,
    bmc, and microsoft teams and the number of events pulled from
    dnac and prime
    this is the page that will load once the user has logged in
    and entered all the credentials'''
    #check if all fields were filled out on settings page
    required_keys = ["dnac", "prime", "epnm", "aci", "bmc", "mksft_teams"]
    for key in required_keys:
        if key not in session:
            #if a field was not filled out, reload settings page
            return redirect(url_for('portal.settings'))

    #get connection status of dnac, prime, bmc, and microsoft teams
    dnac_status = checkIp(session["dnac"]["dnac_host"])
    prime_status = checkIp(session["prime"]["prime_host"])
    epnm_status = checkIp(session["epnm"]["epnm_host"])
    aci_status = checkIp(session["aci"]["aci_host"])
    bmc_status = checkIp(session["bmc"]["bmc_host"])
    mksft_teams_status = session['mksft_teams'].get('webhook_url', "") != ""

    #flask session is immutable, so we have to reassign its value to change it
    dnac = session["dnac"]
    prime = session["prime"]
    epnm = session["epnm"]
    aci = session["aci"]
    bmc = session["bmc"]
    mksft_teams = session["mksft_teams"]

    dnac["events"] = []
    prime["events"] = []
    epnm["events"] = []
    aci["events"] = []

    dnac["status"] = dnac_status
    prime["status"] = prime_status
    epnm["status"] = epnm_status
    aci["status"] = aci_status
    bmc["status"] = bmc_status
    mksft_teams["status"] = mksft_teams_status

    session["dnac"] = dnac
    session["prime"] = prime
    session["epnm"] = epnm
    session["aci"] = aci

    if 'events' in session['dnac'] or 'events' in session['prime'] or 'events' in session['epnm'] or 'events' in session['aci']:
        return render_template('portal/home.html', dnac_status=dnac_status,
                prime_status=prime_status, epnm_status=epnm_status, aci_status=aci_status, bmc_status=bmc_status,
                mksft_teams_status=mksft_teams_status,
                dnac_events=[],
                prime_events=[], epnm_events=[], aci_events=[])

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
    epnm = {}
    aci = {}
    bmc = {}
    mksft_teams = {}

    if 'dnac' in session:
        dnac = session['dnac']
    if 'prime' in session:
        prime = session['prime']
    if 'epnm' in session:
        epnm = session['epnm']
    if 'aci' in session:
        aci = session['aci']
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

        # Check for any EPNM inputs
        if request.form.get('epnm_host') != "":
            epnm["epnm_host"] = request.form.get('epnm_host')
        else:
            epnm["epnm_host"] = 'No-host'
        if request.form.get('epnm_username') != "":
            epnm["epnm_username"] = request.form.get('epnm_username')
        else:
            epnm["epnm_username"] = 'No-user'
        if request.form.get('epnm_password') != "":
            epnm["epnm_password"] = request.form.get('epnm_password')
        else:
            epnm["epnm_password"] = 'No-pass'
        session['epnm'] = epnm

        # Check for any ACI inputs
        if request.form.get('aci_host') != "":
            aci["aci_host"] = request.form.get('aci_host')
        else:
            aci["aci_host"] = 'No-host'
        if request.form.get('aci_username') != "":
            aci["aci_username"] = request.form.get('aci_username')
        else:
            aci["aci_username"] = 'No-user'
        if request.form.get('aci_password') != "":
            aci["aci_password"] = request.form.get('aci_password')
        else:
            aci["aci_password"] = 'No-pass'
        session['aci'] = aci

        # Check for any BMC inputs
        if request.form.get('bmc_host') != "":
            bmc["bmc_host"] = request.form.get('bmc_host')
        else:
            bmc["bmc_host"] = 'No-Host'
        if request.form.get('bmc_username') != "":
            bmc["bmc_username"] = request.form.get('bmc_username')
        else:
            bmc["bmc_username"] = 'No-User'
        if request.form.get('bmc_password') != "":
            bmc["bmc_password"] = request.form.get('bmc_password')
        else:
            bmc["bmc_password"] = 'No-Pass'
        session['bmc'] = bmc
        if 'bmc' in session and session['bmc'] != {}:
            bmc_token = get_Bmc_Token(bmc)
            bmc["bmc_Token"] = bmc_token
            session["bmc"] = bmc

        # Check for any Microsoft Teams inputs
        if request.form.get('webhook_url') != "":
            mksft_teams['webhook_url'] = request.form.get('webhook_url')
        else:
            mksft_teams["webhook_url"] = 'No-URL'
        session['mksft_teams'] = mksft_teams

        return redirect(url_for('portal.home'))

    if error is not None:
        flash(error)
    return render_template('portal/settings.html', session=session)


@bp.route('/dnacLogs', methods=('GET',))
@login_required
def dnacLogs():
    #the dnac logs page needs to be passed the dnac events
    dnac_events = session["dnac"]["events"]
    print(dnac_events)
    return render_template('portal/dnacLogs.html', dnac_events=dnac_events)


@bp.route('/primeLogs', methods=('GET',))
@login_required
def primeLogs():
    #the prime logs page needs to be passed the prime events
    prime_events = session["prime"]["events"]
    return render_template('portal/primeLogs.html', prime_events=prime_events)


@bp.route('/epnmLogs', methods=('GET',))
@login_required
def epnmLogs():
    #the EPNM logs page needs to be passed the epnm events
    epnm_events = session["epnm"]["events"]
    return render_template('portal/epnmLogs.html', epnm_events=epnm_events)

@bp.route('/aciLogs', methods=('GET',))
@login_required
def aciLogs():
    #the ACI logs page needs to be passed the epnm events
    aci_events = session["aci"]["events"]
    return render_template('portal/aciLogs.html', aci_events=aci_events)

@bp.route('/events', methods=('GET',))
@login_required
def events():
    '''retrieve the events from dnac and prime, then pull the information
    necessary from those events, create bmc incident tickets, and send
    microsoft teams messages for each event'''
    dnac = session['dnac']
    prime = session['prime']
    epnm = session['epnm']
    aci = session['aci']

    if dnac['status']:
        dnac['events'] = get_Dna_Events(session['dnac'])

    if prime['status']:
        prime['events'] = get_Prime_Events(session['prime'])

    if epnm['status']:
        epnm['events'] = get_Epnm_Events(session['epnm'])
    
    if aci['status']:
        aci['events'] = get_Aci_Events(session['aci'])

    dnac_events = []
    prime_events = []
    epnm_events = []
    aci_events = []
    #parse through object api call retrieved to condense the size of the dnac events
    try:
        for dnac_event in dnac["events"]:
            dnac_evt = {
                "id": dnac_event["eventId"],
                "name": dnac_event["name"],
                "description": dnac_event["description"],
                "severity": dnac_event["severity"],
                "type": "dnac"
            }
            #add sized down event to dnac_events list
            dnac_events.append(dnac_evt)
    except Exception as e:
        #if key does not exist in event object, print out error
        print(str(e))
    try:
        #parse through object api call retrieved to condense the size of the prime events
        for prime_event in prime["events"]:
            prime_evt = {
                "id": prime_event['queryResponse']['entity'][0]['eventsDTO']['@id'],
                "name": prime_event['queryResponse']['entity'][0]['eventsDTO']['condition']['value'],
                "description": prime_event['queryResponse']['entity'][0]['eventsDTO']['description'],
                "severity": prime_event['queryResponse']['entity'][0]['eventsDTO']['severity'],
                "type": "prime"
            }
            #add sized down event to prime_events list
            prime_events.append(prime_evt)

    except Exception as e:
        #if key does not exist in event object, print out error
        print(str(e))


    try:
        #parse through object api call retrieved to condense the size of the EPNM events
        for epnm_event in epnm["events"]:
            epnm_evt = {
                "id": epnm_event['queryResponse']['entity'][0]['eventsDTO']['@id'],
                "name": epnm_event['queryResponse']['entity'][0]['eventsDTO']['condition']['value'],
                "description": epnm_event['queryResponse']['entity'][0]['eventsDTO']['description'],
                "severity": epnm_event['queryResponse']['entity'][0]['eventsDTO']['severity'],
                "type": "epnm"
            }
            #add sized down event to epnm_events list
            epnm_events.append(epnm_evt)

    except Exception as e:
        #if key does not exist in event object, print out error
        print(str(e))

    try:
        #parse through object api call retrieved to condense the size of the ACI events
        for aci_event in aci["events"]:
            aci_evt = {
                "id": aci_event['queryResponse']['entity'][0]['eventsDTO']['@id'],
                "name": aci_event['queryResponse']['entity'][0]['eventsDTO']['condition']['value'],
                "description": aci_event['queryResponse']['entity'][0]['eventsDTO']['description'],
                "severity": aci_event['queryResponse']['entity'][0]['eventsDTO']['severity'],
                "type": "aci"
            }
            #add sized down event to epnm_events list
            aci_events.append(aci_evt)

    except Exception as e:
        #if key does not exist in event object, print out error
        print(str(e))

    dnac["events"] = dnac_events
    prime["events"] = prime_events
    epnm["events"] = epnm_events
    aci["events"] = aci_events

    session['dnac'] = dnac
    session['prime'] = prime
    session['epnm'] = epnm
    session['aci'] = aci

    bmc = session['bmc']
    teams_url = session['mksft_teams']['webhook_url']

    session.modified = True

    #add function calls to multiprocessing queue so api calls are run in parallel
    q.put(lambda: send_Teams_Message(teams_url, dnac_events))
    q.put(lambda: send_Teams_Message(teams_url, prime_events))
    q.put(lambda: send_Teams_Message(teams_url, epnm_events))
    q.put(lambda: send_Teams_Message(teams_url, aci_events))

    events = dnac_events + prime_events + epnm_events + aci_events

    return jsonify(events)


@bp.route('/dnacTicket', methods=('GET', 'POST'))
@login_required
def dnacTicket():
    #generate a BMC Remedy ticket for a DNAC event
    dnac_event = request.json
    bmc = session["bmc"]

    resp = create_Bmc_Incident_Dnac(bmc, dnac_event)

    return resp


@bp.route('/primeTicket', methods=('GET', 'POST'))
@login_required
def primeTicket():
    #generate a BMC Remedy ticket for a Prime event
    prime_event = request.json
    bmc = session["bmc"]

    resp = create_Bmc_Incident_Prime(bmc, prime_event)

    return resp

@bp.route('/epnmTicket', methods=('GET', 'POST'))
@login_required
def epnmTicket():
    #generate a BMC Remedy ticket for an EPNM event
    epnm_event = request.json
    bmc = session["bmc"]

    resp = create_Bmc_Incident_Epnm(bmc, epnm_event)

    return resp


@bp.route('/aciTicket', methods=('GET', 'POST'))
@login_required
def aciTicket():
    #generate a BMC Remedy ticket for an EPNM event
    aci_event = request.json
    bmc = session["bmc"]

    resp = create_Bmc_Incident_Epnm(bmc, aci_event)

    return resp

