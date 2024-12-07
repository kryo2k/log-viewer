"""Holds configuration varaiables pulled from environment."""
import os
import sys
from babel import Locale
from pytz import timezone as loadtimezone
from .lib.authfile import AuthFile

locale = Locale.parse(os.getenv('LOCALE','en_US'))
timezone = loadtimezone(os.getenv('TIMEZONE','US/Eastern'))
auth_enabled = int(os.getenv('AUTH_ENABLED','1')) == 1
auth_file_name = os.getenv('AUTH_FILE','.script-runner-auth')
auth_file = AuthFile(auth_file_name)
watch_file_name = os.getenv('FILE_PATH', None)
index_title = os.getenv('INDEX_TITLE','Home')

if watch_file_name is None:
	print('FILE_PATH variable has not been set correctly.')
	sys.exit(1)
