
import json
import os

from tests.api_gateway import BaseAPIGatewayTestCase

AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID')

class GetPresignedURLTests(BaseAPIGatewayTestCase):

    def test_should_successfully_get_presigned_url(self):
        _data = json.dumps({
            'stack_name': 'EC-NewAccount-ArtifactRegistry-Test',
            'artifact_key': '/e2etest/apigateway/artifact.zip',
            'owner_account_id': AWS_ACCOUNT_ID,
            'aws_region': 'us-east-1',
            'deployment_selector': 'dev'
        })

        response = self._call('POST', f'{self._invoke_url_base}/registry/artifact/presigned_url', None, _data)  # noqa E501
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_should_fail_for_invalid_parameters(self):
        _data = json.dumps({
            'artifact_key': '/e2etest/apigateway/artifact.zip',
            'owner_account_id': AWS_ACCOUNT_ID,
            'aws_region': 'us-east-1',
            'deployment_selector': 'dev'
        })

        response = self._call('POST', f'{self._invoke_url_base}/registry/artifact/presigned_url', None, _data)  # noqa E501
        status_code = response.status_code
        self.assertEqual(status_code, 400)
