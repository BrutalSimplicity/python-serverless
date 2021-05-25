
import json
import os
import pytest

from . import BaseRoute53TestCase
from contextlib import closing

AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID')
STACK_NAME = 'DeleteArtifact-R53-E2E-Test'

class DeleteArtifactTest(BaseRoute53TestCase):

    def setUp(self) -> None:

        _data = json.dumps({
            'stack_name': STACK_NAME,
            'artifact_key': '/e2etest/route53/artifact.zip',
            'owner_account_id': AWS_ACCOUNT_ID,
            'aws_region': 'us-east-1',
            'deployment_selector': 'dev'
        })
        response = self._generate_presigned_url(_data)
        with closing(open("./tests/deployment_packages/landing-zone-integration-test-artifact/LandingZoneTest.zip", 'rb')) as fd:  # noqa E501
            self._upload_deployment_package(fd, json.loads(response.text))

    @pytest.mark.skip(reason="route53 may not be connected, since r53 is now in the activation repo")
    def test_should_successfully_delete_artifact(self):
        ''' test_should_successfully_delete_artifact '''

        arn = f'arn:aws:ec-artifact-registry:us-east-1:{AWS_ACCOUNT_ID}:artifact/{STACK_NAME}/dev'

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
