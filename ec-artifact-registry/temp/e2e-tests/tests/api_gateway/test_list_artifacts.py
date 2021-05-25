import json
import pytest

from contextlib import closing
from tests.api_gateway import BaseAPIGatewayTestCase

STACK_NAME = "List-Artifacts-E2E-API-Gateway-Test"

@pytest.mark.usefixtures("setup_artifact_for_testing")
class ListArtifactTest(BaseAPIGatewayTestCase):

    def setUp(self) -> None:
        artifact_key = "/test/list_artifacts_test.zip"
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

    def test_should_successfully_list_artifacts_by_account(self):
        self.maxDiff = None
        response = self._call(
            'GET',
            f'{self._invoke_url_base}/registry/artifacts',  # noqa E501
            self._boto_auth,
            None,
            {'owner_account_id':1234567890}
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_should_successfully_list_artifacts_by_deployment_selector(self):
        self.maxDiff = None
        response = self._call(
            'GET',
            f'{self._invoke_url_base}/registry/artifacts',  # noqa E501
            self._boto_auth,
            None,
            {'deployment_selector':"dev"}
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def tearDown(self):
        arn = f'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/{STACK_NAME}/dev' # noqa E501

        # delete the artifact
        response = self.delete_artifact(arn)
        self.assertIsNotNone(response)
