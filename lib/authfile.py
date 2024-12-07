"""Class for validating credentials against a file."""
import os
from unittest import TestCase
from unittest.mock import patch, mock_open

class AuthFile:
	"""Object representing a file used for authentication checks."""

	def __init__(self, path, encoding="utf-8"):
		assert isinstance(path, str), 'File path was not a string.'
		assert isinstance(encoding, str), 'Encoding was not a string.'
		self._path = path
		self._encoding = encoding

	@property
	def path(self):
		"""Returns configured path of file."""
		return self._path

	@property
	def exists(self):
		"""Returns True if path exists or False if not."""
		return os.path.exists(self._path)

	def authenticate(self, username, password):
		"""Attempts to authenticate username and password against file."""
		try:
			with open(self._path, 'r', encoding=self._encoding) as f:
				for line in f:
					stored_username, stored_password = line.strip().split(':')
					if stored_username == username and stored_password == password:
						return True
				return False
		except FileNotFoundError:
			pass
		return False

class AuthFileTestCase(TestCase):
	"""TestCase for AuthFile class"""

	def test_constructor_path_required(self):
		"""Test constructing class with a bad path."""
		with self.assertRaises(AssertionError):
			AuthFile(None)

	def test_constructor_encoding_required(self):
		"""Test constructing class with a bad encoding."""
		with self.assertRaises(AssertionError):
			AuthFile("/bad/path.txt", None)

	def test_path_set_on_construction(self):
		"""Tests that the path is set correctly on construction."""
		test_path = '/some/file/path.txt'
		af = AuthFile(test_path)
		self.assertEqual(af.path,test_path)

	@patch("builtins.open", new_callable=mock_open, read_data="test:123456")
	def test_authenticate_valid_1(self, mock_file):
		"""Tests a valid authentication scenario."""
		encoding = "utf-8"
		af = AuthFile('/path/to/open', encoding)
		self.assertTrue(af.authenticate('test','123456'),'Should have authenticated (test:123456).')
		mock_file.assert_called_with('/path/to/open','r',encoding=encoding)

	@patch("builtins.open", new_callable=mock_open, read_data="test:123456")
	def test_authenticate_invalid_1(self, mock_file):
		"""Tests an invalid authentication scenario."""
		encoding = "utf-8"
		af = AuthFile('/path/to/open', encoding)
		self.assertFalse(af.authenticate('test','123457'),'Should not have authenticated (test:123457).')
		mock_file.assert_called_with('/path/to/open','r',encoding=encoding)
