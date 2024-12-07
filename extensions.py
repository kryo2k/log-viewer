"""All extensions required for application functionality."""

import os
from flask import render_template
from flask_httpauth import HTTPBasicAuth
from flask_socketio import SocketIO

from .config import auth_file, auth_enabled, watch_file_name
from .lib.filewatch import FileWatchThread

auth = HTTPBasicAuth()
socketio = SocketIO(cors_allowed_origins='*')
fwthread = FileWatchThread(watch_file_name)
fwthread.start()

@auth.verify_password
def verify_password(username, password):
	"""Method  to check a username and password for validity."""
	if not auth_enabled or auth_file.authenticate(username, password):
		return (username, password)
	return None

@auth.error_handler
def unauthorized():
	"""Endpoint to send users which are unauthorized to."""
	return render_template('unauthorized.html')
