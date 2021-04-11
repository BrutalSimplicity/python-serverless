import unittest
from cloudtools.common.errors import BaseFormattedError

class SomeSillyException(BaseFormattedError):
    fmt = 'Silly error'

class SomePositionalArgumentException(BaseFormattedError):
    fmt = 'Message: {}'

    def __init__(self, message):
        super().__init__(message)

class SomeKeywordArgumentException(BaseFormattedError):
    fmt = 'Message: {message}'

    def __init__(self, message):
        super().__init__(message=message)

class ExceptionTests(unittest.TestCase):

    def test_error_should_work_without_arguments(self):
        self.assertEqual(str(SomeSillyException()), 'Silly error')

    def test_error_should_format_positional_argument(self):
        self.assertEqual(str(SomePositionalArgumentException('test')), 'Message: test')

    def test_error_should_format_keyword_arguments(self):
        self.assertEqual(str(SomeKeywordArgumentException('test')), 'Message: test')
