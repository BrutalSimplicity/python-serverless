
import json
import unittest

from shared.artifact_registry.models import PresignedURLRequest

class PresignedURLRequestTest(unittest.TestCase):

    def test_successfully_populate_request(self):
        event = json.load(open('./tests/artifact_registry/testdata/request.json'))
        presigned_url_request = PresignedURLRequest(**event)
        self.assertIsNotNone(presigned_url_request)
        self.assertEqual(presigned_url_request.resource, '/registry')
        self.assertEqual(presigned_url_request.path, '/registry/presigned_url')
        body = presigned_url_request.body
        self.assertEqual(body.get('stack_name'), 'Landing-Zone-Test')
        self.assertEqual(body.get('artifact_key'), '/e2e-test/LandingZoneTest.zip')
        self.assertEqual(body.get('owner_account_id'), '775698200277')

    def test_successfully_populate_request_2(self):
        event = json.load(open('./tests/artifact_registry/testdata/presigned_url_request.2.json'))
        presigned_url_request = PresignedURLRequest(**event)
        self.assertIsNotNone(presigned_url_request)
        self.assertEqual(presigned_url_request.resource, '/registry/artifact/presigned_url')
        self.assertEqual(presigned_url_request.path, '/registry/artifact/presigned_url')
        body = presigned_url_request.body
        self.assertEqual(body.get('stack_name'), 'Self-Dependent-Test')
        self.assertEqual(body.get('artifact_key'), '/test/artifact.zip')
        self.assertEqual(body.get('owner_account_id'), '1234567890')
