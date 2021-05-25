import pytest

import requests
from requests.auth import HTTPBasicAuth
from . import BaseRoute53TestCase

class ExpectedFailureTests(BaseRoute53TestCase):

    @pytest.mark.skip(reason="route53 may not be connected, since r53 is now in the activation repo")
    def test_should_fail_for_unauthenticated(self):
        ''' test_should_fail_for_unauthenticated '''

        response = self._call(
            'GET',
            f'https://{self._base_url_r53}/registry/deployment_plan?deployment_selector=dev',
            HTTPBasicAuth('not', 'real'),
            None
        )
        status_code = response.status_code
        self.assertEqual(status_code, 403)

    @pytest.mark.skip(reason="route53 may not be connected, since r53 is now in the activation repo")
    def test_should_fail_for_http(self):
        ''' test_should_fail_for_http '''

        with self.assertRaises(requests.ConnectionError):
            self._call(
                'GET',
                f'http://{self._base_url_r53}/registry/deployment_plan?deployment_selector=dev',
                None,
                None
            )
