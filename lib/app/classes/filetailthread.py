"""Class to watch a file for changes."""
from unittest import TestCase

from app.classes.filewatchthread import FileWatchThread

def readChunk(path, start, end, encoding='utf-8'):
	"""Reads an a chunk from a file."""
	assert isinstance(path, str), 'Path was not an string.'
	assert isinstance(start, int), 'Start position was not an integer.'
	assert isinstance(end, int), 'End position was not an integer.'
	try:
		with open(path, 'r', encoding=encoding) as fp:
			fp.seek(start)
			return fp.read(end - start)
	except (PermissionError, FileNotFoundError, ):
		return ''

class FileTailThread(FileWatchThread):
	"""Thread to monitor the tail-end of a file."""
	def __init__(self, path, maxTailSize=20000):
		super().__init__(path)
		self._tail = ""
		self._encoding = 'utf-8'
		self.maxTailSize = maxTailSize
		self._updateTail(self.fileAccess)

	@property
	def maxTailSize(self):
		"""Gets the max tail size."""
		return self._maxTailSize
	@maxTailSize.setter
	def maxTailSize(self, value):
		"""Sets the max tail size."""
		self._maxTailSize = value if isinstance(value, int) and value >= 0 else 20000

	@property
	def tail(self):
		"""Gets the current tail."""
		return self._tail

	def _computeTailChunkOffset(self, access):
		"""Determines to offsets for a chunk based on access provided."""
		if not access.exists:
			return None
		tailsize = min(access.size, self.maxTailSize)
		end = access.size
		if end < tailsize:
			return (0, end)
		return (end - tailsize, end)

	def _updateTail(self, access, triggerUpdate=True):
		"""Updates tail based on access provided"""
		chunk = self._computeTailChunkOffset(access)
		if chunk is None:
			self._tail = ""
			self._onResetTail()
			return
		start, end = chunk
		self._tail = readChunk(self.path, start, end, self._encoding)
		if triggerUpdate:
			self._onUpdateTail(self._tail)

	def _onDeleted(self, currentFileAccess, previousFileAccess):
		"""Class method called when path is deleted."""
		self._updateTail(currentFileAccess)
		super()._onDeleted(currentFileAccess, previousFileAccess)

	def _onCreated(self, currentFileAccess, previousFileAccess):
		"""Class method called when path is created."""
		self._updateTail(currentFileAccess)
		super()._onCreated(currentFileAccess, previousFileAccess)

	def _onChanged(self, currentFileAccess, previousFileAccess):
		"""Class method called when path is changed."""
		triggerUpdate = True
		sizeA = currentFileAccess.size
		sizeB = previousFileAccess.size
		if sizeA > sizeB:
			self._onConcatTail(readChunk(self.path, sizeB, sizeA, self._encoding))
			triggerUpdate = False
		self._updateTail(currentFileAccess, triggerUpdate)
		super()._onChanged(currentFileAccess, previousFileAccess)

	def _onResetTail(self):
		"""Class method called when tail is reset."""
		self._trigger('reset_tail')

	def _onUpdateTail(self, tail):
		"""Class method called when tail is updated."""
		self._trigger('update_tail', tail)

	def _onConcatTail(self, partial):
		"""Class method called when concatenating to tail."""
		self._trigger('concat_tail', partial)

class FileTailThreadTestCase(TestCase):
	"""TestCase for FileTailThread class"""

	def test_constructor(self):
		"""Test constructing class."""
		self.assertIsInstance(FileTailThread('/bad/path'), FileTailThread)
