
import json
from contextlib import closing
from tests.api_gateway import BaseAPIGatewayTestCase

STACK_NAME = "Delete-Artifact-E2E-API-Gateway-Test"

class DeleteArtifactTest(BaseAPIGatewayTestCase):

    def setUp(self) -> None:
        artifact_key = "/test/artifact.zip"
        owner_account_id = "1234567890"
        deployment_selector = "dev"
        aws_region = "us-east-1"

        _data = json.dumps({
            "stack_name": STACK_NAME,
            "artifact_key": artifact_key,
            "owner_account_id": owner_account_id,
            "deployment_selector": deployment_selector,
            "aws_region": aws_region
        })
        response = self._generate_presigned_url(_data)

        assert response.status_code == 200
        with closing(open("./tests/deployment_packages/landing-zone-integration-test-artifact/LandingZoneTest.zip", 'rb')) as fd:  # noqa E501
            etag = self._upload_deployment_package(fd, json.loads(response.text))

    def test_should_successfully_delete_artifact(self):
        arn = f'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/{STACK_NAME}/dev'

        # test to see if the artifact exists before we delete it
        describe_artifact_response = self.describe_artifact(arn)
        self.assertEqual(describe_artifact_response.status_code, 200)

        # delete the artifact
        response = self.delete_artifact(arn)
        self.assertIsNotNone(response)

        # HTTP status should be 201 - Accepted
        self.assertEqual(response.status_code, 201)

        # Check to see if it was really deleted, should get a 404
        describe_artifact_response = self.describe_artifact(arn)
        self.assertEqual(describe_artifact_response.status_code, 404)
