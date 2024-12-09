"""Class for managing subscribers of events"""
from unittest import TestCase
from unittest.mock import MagicMock

class EventManager:
	"""Holds subscribers of specific event behavior."""

	def __init__(self):
		"""Initializes class"""
		self._handlers = {}

	def register(self, event_name, handler):
		"""Registers a new event handler."""
		assert isinstance(event_name, str), 'Event name was not a string.'
		assert callable(handler), 'Handler was not callable.'
		if event_name not in self._handlers:
			self._handlers[event_name] = []
		self._handlers[event_name].append(handler)

	def trigger(self, event_name, *args, **kwargs):
		"""Calls all handlers subcribed to an event."""
		assert isinstance(event_name, str), 'Event name was not a string.'
		if event_name in self._handlers:
			for handler in self._handlers[event_name]:
				handler(*args, **kwargs)

class EventManagerTestCase(TestCase):
	"""TestCase for EventManager class"""

	def test_constructor(self):
		"""Test constructing class (no arguments)."""
		self.assertIsInstance(EventManager(), EventManager)

	def test_registering_invalid_event(self):
		"""Test that non-string event_name will raise exception"""
		with self.assertRaises(AssertionError):
			em = EventManager()
			em.register(None, None)

	def test_registering_invalid_handler(self):
		"""Test that non-callable handlers will raise exception"""
		with self.assertRaises(AssertionError):
			em = EventManager()
			em.register('test', None)

	def test_registering_valid_handler(self):
		"""Test that callable handler will not raise exception"""
		em = EventManager()
		em.register('test', lambda: None)

	def test_trigger_with_event_handler(self):
		"""Test that callable handler gets invoked on an event."""
		eh = MagicMock(return_value=None)
		em = EventManager()
		em.register('test', eh)
		eh.assert_not_called()
		em.trigger('test',3,4,5,key='value')
		eh.assert_called_with(3,4,5,key="value")

	def test_trigger_without_event_handler(self):
		"""Test that callable handler does not get invoked on a different event."""
		eh = MagicMock(return_value=None)
		em = EventManager()
		em.register('test_x', eh)
		eh.assert_not_called()
		em.trigger('test')
		eh.assert_not_called()
