"""Class to watch a file for changes."""
import os
from unittest import TestCase

class FileAccess:
	"""Information captured from a single access to a file"""
	def __init__(self, path):
		self._path = path
		self._exists = os.access(path, os.R_OK)
		try:
			self._stat = os.stat(path)
		except (PermissionError, FileNotFoundError, ):
			self._stat = None
	@property
	def path(self):
		"""Returns file path."""
		return self._path
	@property
	def exists(self):
		"""Returns recorded existing status."""
		return self._exists
	@property
	def accessTime(self):
		"""Returns recorded stat.st_atime properties."""
		return self._stat.st_atime if self._stat is not None else 0
	@property
	def modifiedTime(self):
		"""Returns recorded stat.st_mtime properties."""
		return self._stat.st_mtime if self._stat is not None else 0
	@property
	def createTime(self):
		"""Returns recorded stat.st_ctime properties."""
		return self._stat.st_ctime if self._stat is not None else 0
	@property
	def size(self):
		"""Returns recorded stat.st_ctime properties."""
		return self._stat.st_size if self._stat is not None else 0
	def __eq__(self, other):
		return self.exists == other.exists and self.modifiedTime == other.modifiedTime

class FileAccessTestCase(TestCase):
	"""TestCase for FileAccess class"""

	def test_constructor(self):
		"""Test constructing class."""
		self.assertIsInstance(FileAccess('/bad/path'), FileAccess)
