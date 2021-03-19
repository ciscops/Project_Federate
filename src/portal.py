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

    if error is not None:
        flash(error)
    return render_template('portal/home.html')


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    """
    Settings Page back-end functionality
    NOTE: NOT FULLY IMPLEMENTED!!! PLACEHOLDER FOR FUTURE RELEASE
    :return:
    """
    error = None

    return render_template('portal/settings.html', session=session)
