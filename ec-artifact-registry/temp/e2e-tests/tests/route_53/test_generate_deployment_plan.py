import pytest

from . import BaseRoute53TestCase

class GetPresignedURLTests(BaseRoute53TestCase):

    @pytest.mark.skip(reason="route53 may not be connected, since r53 is now in the activation repo")
    def test_should_successfully_generate_deployment_plan(self):
        ''' test_should_successfully_generate_deployment_plan '''

        response = self._call('GET', f'https://{self._base_url_r53}/registry/deployment_plan?deployment_selector=dev', self._auth, None)  # noqa E501
        self._validate_response(response)

    @pytest.mark.skip(reason="route53 may not be connected, since r53 is now in the activation repo")
    def test_should_fail_for_invalid_request(self):
        ''' test_should_fail_for_invalid_request '''

        response = self._call('GET', f'https://{self._base_url_r53}/registry/deployment_plan', self._auth, None)  # noqa E501
        self._validate_response(response, 400)
