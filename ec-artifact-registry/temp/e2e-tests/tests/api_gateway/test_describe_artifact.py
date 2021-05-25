import json
import pytest

from tests.api_gateway import BaseAPIGatewayTestCase

STACK_NAME = "Describe-Artifact-E2E-API-Gateway-Test"

@pytest.mark.usefixtures("setup_artifact_for_testing")
class DescribeArtifactTest(BaseAPIGatewayTestCase):

    def test_should_successfully_describe_artifact(self):
        self.maxDiff = None
        response = self._call(
            'GET',
            f'{self._invoke_url_base}/registry/artifact',  # noqa E501
            self._boto_auth,
            None,
            {'arn': f'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/{STACK_NAME}/dev'}
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        artifact = json.loads(response.text)
        self.assertIsNotNone(artifact)
        self.assertEqual(artifact.get('stack_name'), STACK_NAME)
        self.assertEqual(artifact.get('artifact_key'), '/test/artifact.zip')
        self.assertEqual(artifact.get('owner_account_id'), '1234567890')
        self.assertEqual(artifact.get('dependent_artifacts'), None)
        self.assertEqual(artifact.get('deployment_selector'), 'dev')
        self.assertEqual(artifact.get('manifest_template'), "{'Template': {'Name': 'LandingZoneTest.yml'}, 'CloudFormation': {'RequestKWArgs': {'StackName': 'landing-zone-e2e-test', 'Capabilities': ['CAPABILITY_IAM']}}, 'Targets': {'AccountIds': [775698200277]}, 'Regions': ['us-east-1']}")  # noqa E501
        self.assertEqual(artifact.get('aws_region'), 'us-east-1')
        self.assertEqual(artifact.get('arn'), f'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/{STACK_NAME}/dev')  # noqa E501

    def test_should_get_404_for_not_found_artifact(self):
        response = self._call(
            'GET',
            f'{self._invoke_url_base}/registry/artifact',  # noqa E501
            self._boto_auth,
            None,
            {'arn': 'missing'}
        )
        status_code = response.status_code
        self.assertEqual(status_code, 404)
