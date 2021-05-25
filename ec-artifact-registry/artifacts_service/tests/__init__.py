import botocore
import json
import os
import sys
import unittest

from unittest import mock

sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', 'src'))


class BaseUnitTestCase(unittest.TestCase):

    def setUp(self):
        pass
    #     self.environ = {}
    #     self.environ_patch = mock.patch('os.environ', self.environ)
    #     self.environ_patch.start()

    # def tearDown(self):
    #     self.environ_patch.stop()

    # def _validate_response(self, response):
    #     self.assertIsNotNone(response)
