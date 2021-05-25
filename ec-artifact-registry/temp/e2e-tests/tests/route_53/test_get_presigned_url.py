
import json
import os
import pytest

from . import BaseRoute53TestCase

AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID')

class GetPresignedURLTests(BaseRoute53TestCase):

    @pytest.mark.skip(reason="route53 may not be connected, since r53 is now in the activation repo")
    def test_should_successfully_get_presigned_url(self):
        ''' test_should_successfully_get_presigned_url '''

        _data = json.dumps({
            'stack_name': 'EC-NewAccount-ArtifactRegistry-Test',
            'artifact_key': '/e2etest/route53/artifact.zip',
            'owner_account_id': AWS_ACCOUNT_ID,
            'aws_region': 'us-east-1',
            'deployment_selector': 'dev'
        })

        response = self._call(
            'POST',
            f'https://{self._base_url_r53}/registry/artifact/presigned_url',
            self._auth, _data
        )
        self._validate_response(response)
