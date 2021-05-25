
import pytest
import requests
from requests.auth import HTTPBasicAuth
from . import BaseAPIGatewayTestCase

class ExpectedFailureTests(BaseAPIGatewayTestCase):
    '''
        Test Cases that exercise expected failures
        - authentication

    '''

    def test_should_fail_for_unauthenticated(self):
        ''' This test ensures that the Authentication is working '''

        response = self._call(
            'GET',
            f'{self._invoke_url_base}/registry/deployment_plan?deployment_selector=dev',
            HTTPBasicAuth('not', 'real'),
            None
        )
        status_code = response.status_code
        self.assertEqual(status_code, 403)

    def test_should_fail_for_http(self):
        ''' This test ensures that https is enforced '''

        with self.assertRaises(requests.ConnectionError):
            self._call(
                'GET',
                f'http://{self._base_url}/{self._deploy_environment}/registry/deployment_plan?deployment_selector=dev',
                HTTPBasicAuth('not', 'real'),
                None
            )

    def test_should_get_404_for_unmatched_request(self):
        ''' This test ensures that... '''

        response = self._call(
            'GET',
            f'{self._invoke_url_base}/registry/not',
            None,
            None
        )
        status_code = response.status_code
        self.assertEqual(status_code, 404)
