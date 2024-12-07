"""Main blueprint for interacting with application reader."""

import io
import os
from flask import Blueprint, render_template
from flask_socketio import emit
from ..extensions import auth, socketio, fwthread
from ..config import index_title

bp = Blueprint("app_index", __name__)
max_buffer_size = 20000

@bp.route("/")
@auth.login_required
def index():
	"""Main UI."""
	return render_template('index.html',
		page_title=index_title,
		fwthread=fwthread,
		maxBufferSize=max_buffer_size)

def readFileTail(tailSize=max_buffer_size, encoding='utf-8'):
	"""Reads the tail of a file."""
	try:
		with open(fwthread.path, 'r', encoding=encoding) as file:
			file.seek(0, io.SEEK_END)
			file_size = file.tell()
			file.seek(max(0, min(file_size, file_size - tailSize)))
			return file.read()
	except (PermissionError, FileNotFoundError, ):
		return ''

def readFileOffset(startOffset, endOffset, encoding='utf-8'):
	"""Reads a part of the file."""
	try:
		with open(fwthread.path, 'r', encoding=encoding) as file:
			file.seek(startOffset)
			return file.read(endOffset - startOffset)
	except (PermissionError, FileNotFoundError, ):
		return ''

try:
	fileSize = fwthread.pathStat.st_size # in bytes
	fileTail = readFileTail()
	fileCursor = fileSize
except (PermissionError, FileNotFoundError, ):
	fileSize = 0
	fileTail = ""
	fileCursor = 0

@fwthread.on('created')
def fwthread_created():
	"""Event called when file watch thread detects file being created."""
	global fileTail, fileSize, fileCursor
	try:
		fileSize = fwthread.pathStat.st_size # in bytes
		fileTail = readFileTail()
		fileCursor = fileSize
		socketio.emit('switchExisting')
		socketio.emit('replaceContent', fileTail)
	except (PermissionError, FileNotFoundError, ):
		fileSize = 0
		fileTail = ""
		fileCursor = 0
		socketio.emit('switchMissing')
		socketio.emit('replaceContent', '')

@fwthread.on('changed')
def fwthread_changed():
	"""Event called when file watch thread detects file changed."""
	global fileTail, fileSize, fileCursor
	try:
		fileTail = readFileTail()
		newFileSize = fwthread.pathStat.st_size # in bytes
		if newFileSize < fileSize:
			socketio.emit('replaceContent', fileTail)
		elif newFileSize > fileSize:
			socketio.emit('appendContent', readFileOffset(fileCursor, newFileSize))
		fileSize = newFileSize
		fileCursor = newFileSize
	except (PermissionError, FileNotFoundError, ):
		fileSize = 0
		fileTail = ""
		fileCursor = 0
		socketio.emit('switchMissing')
		socketio.emit('replaceContent', '')

@fwthread.on('deleted')
def fwthread_deleted():
	"""Event called when file watch thread detects file deleted."""
	global fileTail, fileSize, fileCursor
	fileTail = ""
	fileSize = 0
	fileCursor = 0
	socketio.emit('switchMissing')
	socketio.emit('replaceContent', '')

@socketio.on('connect')
def client_connect(_auth):
	"""Event called when client connects to socket.io"""
	emit('replaceContent', fileTail)
	if fwthread.pathExists:
		emit('switchExisting')
	else:
		emit('switchMissing')

# @socketio.on('disconnect')
# def client_disconnect():
# 	"""Event called when client disconnects from socket.io"""
