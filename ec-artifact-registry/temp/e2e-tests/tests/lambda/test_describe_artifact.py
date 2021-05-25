import json
import pytest
from . import BaseLambdaTestCase


@pytest.mark.usefixtures("setup_artifact_for_testing")
class DescribeArtifact(BaseLambdaTestCase):

    def test_should_successfully_describe_artifact(self):
        ''' test_should_successfully_describe_artifact '''

        _data = json.dumps({
            "resource": "/registry/artifact",
            "path": "/registry/artifact",
            "queryStringParameters": {
                "arn": "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Describe-Artifact-E2E-Test/dev"
            },
            "httpMethod": "GET",
            "isBase64Encoded": False
        })
        response = self._call(_data, self._describe_artifact_function_name)
        _payload = response['Payload']
        payload = json.loads(_payload.read().decode('utf8'))
        # did we get a successful status code?
        self.assertEqual(payload.get('statusCode'), 200)
        body = json.loads(payload.get('body'))
        self.assertEqual(body.get('stack_name'), 'Describe-Artifact-E2E-Test')
        self.assertEqual(body.get('artifact_key'), '/test/artifact.zip')
        self.assertEqual(body.get('owner_account_id'), '1234567890')
        self.assertEqual(body.get('dependent_artifacts'), None)
        self.assertEqual(body.get('deployment_selector'), 'dev')
        self.assertEqual(body.get('manifest_template'), "{'Template': {'Name': 'LandingZoneTest.yml'}, 'CloudFormation': {'RequestKWArgs': {'StackName': 'landing-zone-e2e-test', 'Capabilities': ['CAPABILITY_IAM']}}, 'Targets': {'AccountIds': [775698200277]}, 'Regions': ['us-east-1']}")  # noqa E501
        self.assertEqual(body.get('aws_region'), 'us-east-1')
        self.assertEqual(body.get('arn'), 'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Describe-Artifact-E2E-Test/dev')  # noqa E501

    def test_should_return_404_for_nonexistent_artifact(self):
        ''' test_should_return_404_for_nonexistent_artifact '''

        _data = json.dumps({
            "resource": "/registry/artifact",
            "path": "/registry/artifact",
            "queryStringParameters": {
                "arn": "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Artifact-That-Does-Not-Exist/dev"
            },
            "httpMethod": "GET",
            "isBase64Encoded": False
        })
        response = self._call(_data, self._describe_artifact_function_name)
        _payload = response['Payload']
        payload = json.loads(_payload.read().decode('utf8'))
        # did we get the expected status code?
        self.assertEqual(payload.get('statusCode'), 404)
