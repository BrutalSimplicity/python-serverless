
import base64
import json
from . import BaseLambdaTestCase

class GetPresignedUrlLambdaTests(BaseLambdaTestCase):
    """E2E Tests that call the Lambda"""

    def test_should_successfully_get_presigned_url(self):
        stack_name = "EC-LandingZone-Integration-Test-EC-8996"
        artifact_key = "/test/artifact.zip"
        owner_account_id = "1234567890"
        deployment_selector = "dev"
        aws_region = "us-east-1"
        _data = json.dumps({
            "resource": "/registry/artifact/presigned_url",
            "path": "/registry/artifact/presigned_url",
            "httpMethod": "POST",
            "body": {
                "stack_name": stack_name,
                "artifact_key": artifact_key,
                "owner_account_id": owner_account_id,
                "deployment_selector": deployment_selector,
                "aws_region": aws_region
            },
            "isBase64Encoded": False
        })
        response = self._call(_data, self._get_presigned_url_function_name)
        _payload = response['Payload']
        payload = json.loads(_payload.read().decode('utf8'))
        # did we get a successful status code?
        self.assertEqual(payload.get('statusCode'), 200)

        # did we get the response we expected?
        body = json.loads(payload['body'])
        fields = body['fields']
        # metadata is stored in the x-amz-meta-artifact header.  This is stored with the s3 object when it is posted.
        x_meta_artifact_encoded = fields['x-amz-meta-artifact']
        x_meta_artifact = json.loads(base64.b64decode(x_meta_artifact_encoded).decode('utf-8'))
        self.assertEqual(stack_name, x_meta_artifact['stack_name'])
        self.assertEqual(owner_account_id, x_meta_artifact['owner_account_id'])
        self.assertEqual(deployment_selector, x_meta_artifact['deployment_selector'])

    def test_should_fail_when_self_dependent(self):
        ''' When an artifact has its own arn as a dependent artifact. '''
        stack_name = "Self-Dependent-Test"
        artifact_key = "/test/artifact.zip"
        owner_account_id = "1234567890"
        deployment_selector = "dev"
        aws_region = "us-east-1"

        _data = json.dumps({
            "resource": "/registry/artifact/presigned_url",
            "path": "/registry/artifact/presigned_url",
            "httpMethod": "POST",
            "body": {
                "stack_name": stack_name,
                "artifact_key": artifact_key,
                "owner_account_id": owner_account_id,
                "deployment_selector": deployment_selector,
                "dependent_artifacts": [
                    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Self-Dependent-Test/dev"
                ],
                "aws_region": aws_region
            },
            "isBase64Encoded": False
        })
        response = self._call(_data, self._get_presigned_url_function_name)
        _payload = response['Payload']
        payload = json.loads(_payload.read().decode('utf8'))
        # did we get an expected status code?
        self.assertEqual(payload.get('statusCode'), 400)
