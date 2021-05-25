
import os

from tests.api_gateway import BaseAPIGatewayTestCase

AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID')

class GenerateDeploymentPlanTests(BaseAPIGatewayTestCase):

    def test_should_successfully_generate_deployment_plan(self):

        response = self._call('GET', f'{self._invoke_url_base}/registry/deployment_plan?deployment_selector=dev', None, None)  # noqa E501
        status_code = response.status_code
        self.assertEqual(status_code, 200)
