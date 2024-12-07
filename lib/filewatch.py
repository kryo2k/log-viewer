"""Class to watch a file for changes."""
import time
import os
from threading import Thread, Lock
from unittest import TestCase

from .eventmanager import EventManager

class FileWatchThread(Thread):
	"""Thread class for watching a file for changes."""
	def __init__(self, path):
		assert isinstance(path, str), 'Expected path argument to be a string.'
		super().__init__(target=self.__threadloop, daemon=True)
		self._path = path
		self._pathExisted = os.path.exists(path)
		self._eventManager = EventManager()
		self._pollInterval = 0.1
		self._cachedStamp = None
		self._checkLock = Lock()

	@property
	def path(self):
		"""Virtual property to access path setting."""
		return self._path

	@property
	def pathExists(self):
		"""Virtual property to check if path exists."""
		return os.path.exists(self._path) and self.pathAccess()

	@property
	def pathStat(self):
		"""Virtual property to access stat of path setting."""
		return os.stat(self._path)

	@property
	def lastModified(self):
		"""Virtual property to access stat of path setting."""
		return self._cachedStamp

	def pathAccess(self, mode=os.R_OK):
		"""Verifies access to the current file."""
		return os.access(self._path, mode)
	
	def __threadloop(self):
		"""Internal loop called in thread"""
		while True:
			with self._checkLock:
				try:
					mtime = self.pathStat.st_mtime
					self.pathAccess()
					if not self._pathExisted:
						self._eventManager.trigger('created')
					elif mtime != self._cachedStamp:
						self._eventManager.trigger('changed')
					self._pathExisted = True
					self._cachedStamp = mtime
				except (PermissionError, FileNotFoundError, ):
					if self._pathExisted:
						self._eventManager.trigger('deleted')
					self._cachedStamp = None
					self._pathExisted = False
			time.sleep(self._pollInterval)

	def on(self, event_name):
		"""Decorator function to get access to file watch thread events."""
		def decorator(func):
			self._eventManager.register(event_name, func)
			return func
		return decorator

class FileWatchThreadTestCase(TestCase):
	"""TestCase for FileWatchThread class"""

	def test_constructor(self):
		"""Test constructing class (no arguments)."""
		self.assertIsInstance(FileWatchThread('/bad/path'), FileWatchThread)
