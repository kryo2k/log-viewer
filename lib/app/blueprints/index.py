"""Main blueprint for interacting with application reader."""

from flask import Blueprint, render_template
from flask_socketio import emit
from app.extensions import auth, socketio, ftthread
from app.config import index_title

bp = Blueprint("app_index", __name__)

@bp.route("/")
@auth.login_required
def index():
	"""Main UI."""
	return render_template('index.html',
		page_title=index_title,
		thread=ftthread)

@ftthread.on('concat_tail')
def ftthread_concat_tail(partial):
	"""Event called tail has new content added."""
	socketio.emit('appendContent', partial)

@ftthread.on('update_tail')
def ftthread_update_tail(tail):
	"""Event called tail is updated with content (not-blanked)"""
	socketio.emit('replaceContent', tail)
	socketio.emit('switchExisting')

@ftthread.on('reset_tail')
def ftthread_reset_tail():
	"""Event called tail is reset (blanked)"""
	socketio.emit('replaceContent', '')
	socketio.emit('switchMissing')

@socketio.on('connect')
def client_connect(_auth):
	"""Event called when client connects to socket.io"""
	emit('replaceContent', ftthread.tail)
	if ftthread.fileAccess.exists:
		emit('switchExisting')
	else:
		emit('switchMissing')

# @socketio.on('disconnect')
# def client_disconnect():
# 	"""Event called when client disconnects from socket.io"""
