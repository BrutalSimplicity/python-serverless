
import base64
import json
import os

from . import BaseLambdaTestCase

AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID')
SWA_ENVIRONMENT = os.environ.get('SWA_ENVIRONMENT', 'dev')


class ArtifactRegistryUpdaterTests(BaseLambdaTestCase):
    """E2E Tests that call the Lambda"""

    def test_should_successfully_process_registry_artifact(self):
        stack_name = "Landing-Zone-Test"
        artifact_key = "/e2e-test/LandingZoneTest.zip"
        owner_account_id = AWS_ACCOUNT_ID
        deployment_selector = SWA_ENVIRONMENT
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

        with open("./tests/deployment_packages/landing-zone-integration-test-artifact/LandingZoneTest.zip", 'rb') as fd:
            self.upload_deployment_package(fd, body)
