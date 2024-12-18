"""Main entrypoint for launching project unit tests."""
import unittest

from app.classes import authfile, eventmanager, fileaccess, filewatchthread, filetailthread

test_modules = [
	authfile,
	eventmanager,
	fileaccess,
	filewatchthread,
	filetailthread
]

def suite():
	"""Constructs unittest suite from module testcases."""
	loader = unittest.TestLoader()
	result = unittest.TestSuite()
	for m in test_modules:
		result.addTests(loader.loadTestsFromModule(m))
	return result

def run_suite(verbosity=3):
	"""Runs the unittest suite from module testcases."""
	runner = unittest.TextTestRunner(verbosity=verbosity)
	return runner.run(suite())

if __name__ == '__main__':
	run_suite()
