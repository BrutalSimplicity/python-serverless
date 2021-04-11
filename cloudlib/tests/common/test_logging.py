import unittest
from unittest.mock import patch
import logging


with patch('cloudtools.common.utils.generate_timestamp') as mock_generate_timestamp:
    mock_generate_timestamp.return_value = 'now'
    from cloudtools.common.logging import (
        JsonLogFormatter, log_it, get_logging_context, use_logging_context
    )


class MockLoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG)
        self.log_records = []

    def emit(self, record):
        self.log_records.append(record)

    def get_log_records(self):
        return self.log_records

testLogger = logging.getLogger('test')
testLogger.setLevel(logging.DEBUG)

class LoggingTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.mockHandler = MockLoggingHandler()
        self.mockHandler.setFormatter(JsonLogFormatter())
        testLogger.addHandler(self.mockHandler)

    def tearDown(self):
        testLogger.removeHandler(self.mockHandler)

    def test_should_log_decorated_method(self):

        @log_it(logger=testLogger, level=logging.DEBUG)
        def action():
            pass

        action()

        expected = {
            'event': 'action',
            'message': 'action was called',
            'level': 'DEBUG',
            'caller': 'action',
            'parameters': '()',
            'input': {
                'args': (),
                'kwargs': {}
            },
            'output': None,
            'timestamp': 'now'
        }
        actual = self.mockHandler.get_log_records()[0].msg

        self.assertDictEqual(actual, expected)

    def test_should_log_decorated_method_with_parameters(self):
        @log_it(logger=testLogger, level=logging.DEBUG)
        def action(a, b, c):
            pass

        action(1, 2, 3)

        expected = {
            'event': 'action',
            'message': 'action was called',
            'level': 'DEBUG',
            'caller': 'action',
            'parameters': '(a, b, c)',
            'input': {
                'args': (1, 2, 3),
                'kwargs': {}
            },
            'timestamp': 'now',
            'output': None
        }
        actual = self.mockHandler.get_log_records()[0].msg

        self.assertDictEqual(actual, expected)

    def test_should_log_decorated_method_with_return_value(self):
        @log_it(logger=testLogger, level=logging.DEBUG)
        def action(a, b, c, k1=1, k2=2):
            return {
                'foo': 'bar',
                'bar': 'foo'
            }

        action(1, 2, 3)

        expected = {
            'event': 'action',
            'message': 'action was called',
            'level': 'DEBUG',
            'caller': 'action',
            'parameters': '(a, b, c, k1=1, k2=2)',
            'input': {
                'args': (1, 2, 3),
                'kwargs': {}
            },
            'timestamp': 'now',
            'output': {
                'foo': 'bar',
                'bar': 'foo'
            }
        }
        actual = self.mockHandler.get_log_records()[0].msg

        self.assertDictEqual(actual, expected)

    def test_should_log_decorated_method_with_kwargs(self):
        @log_it(logger=testLogger, level=logging.WARNING)
        def action(a, b, c, **kwargs):
            return {
                'foo': 'bar',
                'bar': 'foo'
            }

        action(1, 2, 3, k4=4, k5=5)

        expected = {
            'event': 'action',
            'message': 'action was called',
            'level': 'WARNING',
            'caller': 'action',
            'parameters': '(a, b, c, **kwargs)',
            'input': {
                'args': (1, 2, 3),
                'kwargs': {
                    'k4': 4,
                    'k5': 5
                }
            },
            'timestamp': 'now',
            'output': {
                'foo': 'bar',
                'bar': 'foo'
            }
        }
        actual = self.mockHandler.get_log_records()[0].msg

        self.assertDictEqual(actual, expected)

    def test_should_log_nested_scopes(self):
        @log_it(logger=testLogger, level=logging.INFO, event='nested_event')
        def nested2(a, b):
            return a + b

        def nested1():
            return nested2(1, 2)

        @log_it(logger=testLogger, level=logging.DEBUG)
        def action(a, b, c, **kwargs):
            result = nested1()
            return {
                'foo': 'bar',
                'bar': 'foo',
                'nested': result
            }

        action(1, 2, 3, k4=4, k5=5)

        expected = [
            {
                'event': 'nested_event',
                'message': 'nested2 was called',
                'level': 'INFO',
                'caller': 'nested2',
                'parameters': '(a, b)',
                'input': {
                    'args': (1, 2),
                    'kwargs': {}
                },
                'timestamp': 'now',
                'output': 3
            },
            {
                'event': 'action',
                'message': 'action was called',
                'level': 'DEBUG',
                'caller': 'action',
                'parameters': '(a, b, c, **kwargs)',
                'input': {
                    'args': (1, 2, 3),
                    'kwargs': {
                        'k4': 4,
                        'k5': 5
                    }
                },
                'timestamp': 'now',
                'output': {
                    'foo': 'bar',
                    'bar': 'foo',
                    'nested': 3
                }
            }
        ]
        actual = [record.msg for record in self.mockHandler.get_log_records()]

        self.assertCountEqual(actual, expected)

    def test_should_log_exception(self):
        error = RuntimeError('oops')
        @log_it(logger=testLogger)
        def action(a, b, c):
            raise error

        with self.assertRaises(RuntimeError):
            action(1, 2, 3)

    def test_should_log_nested_exception_only_once(self):
        error = RuntimeError('oops')

        @log_it(logger=testLogger)
        def nested2(a, b):
            raise error

        def nested1():
            return nested2(1, 2)

        @log_it(logger=testLogger)
        def action(a, b, c):
            nested1()

        with self.assertRaises(RuntimeError):
            action(1, 2, 3)

    def test_should_add_context_metadata(self):

        @log_it(logger=testLogger)
        def inner1():
            return {
                'data': 'inner1'
            }

        @log_it(logger=testLogger)
        def inner2():
            inner1()
            return {
                'data': 'inner2'
            }


        @use_logging_context
        @log_it(logger=testLogger)
        def handler(key):
            context = get_logging_context()
            context.add_metadata('key', key)
            inner2()

        handler('same_scope')

        expected = [
            {
                'event': 'inner1',
                'message': 'inner1 was called',
                'level': 'INFO',
                'caller': 'inner1',
                'parameters': '()',
                'input': {
                    'args': (),
                    'kwargs': {}
                },
                'timestamp': 'now',
                'output': {
                    'data': 'inner1',
                },
                'context': {
                    'key': 'same_scope'
                }
            },
            {
                'event': 'inner2',
                'message': 'inner2 was called',
                'level': 'INFO',
                'caller': 'inner2',
                'parameters': '()',
                'input': {
                    'args': (),
                    'kwargs': {}
                },
                'timestamp': 'now',
                'output': {
                    'data': 'inner2',
                },
                'context': {
                    'key': 'same_scope'
                }
            },
            {
                'event': 'handler',
                'message': 'handler was called',
                'level': 'INFO',
                'caller': 'handler',
                'parameters': '(key)',
                'input': {
                    'args': ('same_scope',),
                    'kwargs': {}
                },
                'timestamp': 'now',
                'output': None,
                'context': {
                    'key': 'same_scope'
                }
            }
        ]

        actual = [record.msg for record in self.mockHandler.get_log_records()]

        self.assertCountEqual(actual, expected)
