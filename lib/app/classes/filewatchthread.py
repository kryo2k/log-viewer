"""Class to watch a file for changes."""
import time
from threading import Thread, Lock
from unittest import TestCase

from app.classes.eventmanager import EventManager
from app.classes.fileaccess import FileAccess

class FileWatchThread(Thread):
	"""Thread to monitor a path for changes."""
	def __init__(self, path):
		assert isinstance(path, str), 'Path was not a string.'
		super().__init__(target=self.__threadLoop, daemon=True)
		self._path = path
		self._pollInterval = 0.1
		self._eventManager = EventManager()
		self._accessLock = Lock()
		self._lastFileAccess = self._createFileAccess()

	@property
	def path(self):
		"""Virtual property to access path setting."""
		return self._path

	@property
	def fileAccess(self):
		"""Virtual property to access lastFileAccess setting."""
		return self._lastFileAccess

	@property
	def pollInterval(self):
		"""Virtual property to access pollInterval setting."""
		return self._pollInterval

	@pollInterval.setter
	def pollInterval(self, value):
		"""Virtual property to update access pollInterval setting."""
		self._pollInterval = value if isinstance(value, (int,float)) else self._pollInterval

	def on(self, event_name):
		"""Decorator function to get access to file watch thread events."""
		def decorator(func):
			self._eventManager.register(event_name, func)
			return func
		return decorator

	def _createFileAccess(self):
		"""Creates a new FileAccess class instance with the current path."""
		return FileAccess(self._path)

	def _trigger(self, event_name, *args, **kwargs):
		self._eventManager.trigger(event_name,*args,**kwargs)

	def _onDeleted(self, currentFileAccess, previousFileAccess):
		"""Class method called when path is deleted."""
		self._trigger('deleted', currentFileAccess, previousFileAccess)

	def _onCreated(self, currentFileAccess, previousFileAccess):
		"""Class method called when path is created."""
		self._trigger('created', currentFileAccess, previousFileAccess)

	def _onChanged(self, currentFileAccess, previousFileAccess):
		"""Class method called when path is changed."""
		self._trigger('changed', currentFileAccess, previousFileAccess)

	def __threadLoop(self):
		"""Internal thread loop"""
		while True:
			with self._accessLock:
				nfa = self._createFileAccess()
				lfa = self._lastFileAccess
				self._lastFileAccess = nfa
				if lfa.exists and not nfa.exists:
					self._onDeleted(nfa,lfa)
				elif not lfa.exists and nfa.exists:
					self._onCreated(nfa,lfa)
				elif lfa != nfa:
					self._onChanged(nfa,lfa)
			time.sleep(self._pollInterval)

class FileWatchThreadTestCase(TestCase):
	"""TestCase for FileWatchThread class"""

	def test_constructor(self):
		"""Test constructing class."""
		self.assertIsInstance(FileWatchThread('/bad/path'), FileWatchThread)
