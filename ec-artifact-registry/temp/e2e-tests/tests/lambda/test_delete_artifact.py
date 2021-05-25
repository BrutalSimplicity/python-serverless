
import json

from . import BaseLambdaTestCase
from contextlib import closing

class DeleteArtifact(BaseLambdaTestCase):

    def setUp(self) -> None:
        stack_name = "Delete-Artifact-E2E-Test"
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
        response = self.generate_presigned_url(_data)
        body = json.loads(response['body'])
        with closing(open("./tests/deployment_packages/landing-zone-integration-test-artifact/LandingZoneTest.zip", 'rb')) as fd:  # noqa E501
            self.upload_deployment_package(fd, body)


    def test_should_successfully_delete_artifact(self):
        arn = "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Delete-Artifact-E2E-Test/dev"
        describe_artifact_response = self.describe_artifact(arn)
        assert describe_artifact_response['statusCode'] == 200

        _data = json.dumps({
            "resource": "/registry/artifact",
            "path": "/registry/artifact",
            "queryStringParameters": {
                "arn": arn
            },
            "httpMethod": "DELETE",
            "isBase64Encoded": False
        })
        response = self._call(_data, self._describe_artifact_function_name)
        self.assertIsNotNone(response)

        _payload = response['Payload']
        payload = json.loads(_payload.read().decode('utf8'))
        assert payload['statusCode'] == 201

        describe_artifact_response = self.describe_artifact(arn)
        assert describe_artifact_response['statusCode'] == 404
