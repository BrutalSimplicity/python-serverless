
import os
import pytest

from . import BaseRoute53TestCase

AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID')

@pytest.mark.usefixtures("setup_artifact_for_testing")
class DescribeArtifactTests(BaseRoute53TestCase):

    @pytest.mark.skip(reason="route53 may not be connected, since r53 is now in the activation repo")
    def test_should_successfully_get_presigned_url(self):
        ''' test_should_successfully_get_presigned_url '''

        response = self._call(
            'GET',
            f'https://{self._base_url_r53}/registry/artifact',
            self._auth,
            None,
            {
                'arn': 'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Describe-Artifact-R53-E2E-Test/dev'  # noqa E501
            }
        )
        self._validate_response(response)
        self.assertEqual(response.status_code, 200)
