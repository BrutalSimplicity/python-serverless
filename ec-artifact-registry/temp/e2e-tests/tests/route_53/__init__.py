
import boto3
import json
import logging
import os
import pytest
import re
import requests
import sys
import time

from aws_requests_auth.aws_auth import AWSRequestsAuth

from tests import (
    BaseTestCase,
)

DEBUG_HTTP = os.getenv('DEBUG_HTTP', False)
# make it empty if not found.  need to fail so we know theres a problem.
AWS_REGION = os.getenv('AWS_REGION', '')
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
DEPLOY_ENVIRONMENT = os.getenv('DEPLOY_ENVIRONMENT')
SWA_ENVIRONMENT = os.getenv('SWA_ENVIRONMENT')
AWS_SERVICE_NAME = 'execute-api'

sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '.', 'shared'))


class BaseRoute53TestCase(BaseTestCase):
    '''BaseRoute53TestCase
    Common methods and resources for Route53-Based Tests
    '''

    @classmethod
    def setUpClass(cls):
        ''' setUpClass '''
        global AWS_ACCESS_KEY
        global AWS_SECRET_ACCESS_KEY
        global AWS_SESSION_TOKEN
        global AWS_REGION
        global AWS_PROFILE
        global DEPLOY_ENVIRONMENT
        global AWS_ACCOUNT_ID
        global SWA_ENVIRONMENT
        deploy_environment = re.sub(
            r'\.',
            '-',
            DEPLOY_ENVIRONMENT
        ).lower()

        if DEPLOY_ENVIRONMENT in ["dev", "qa", "prod"]:
            cls._base_url_r53 = f'api.registry.ec.{SWA_ENVIRONMENT}.aws.swacorp.com'.lower()  # noqa E501
        else:
            cls._base_url_r53 = f'api.{deploy_environment}.registry.ec.{SWA_ENVIRONMENT}.aws.swacorp.com'.lower()  # noqa E501
        cls._invoke_url_r53 = f'https://{cls._base_url_r53}/'
        if AWS_PROFILE is not None:
            # retrieve credentials using a profile
            session = boto3.session.Session(profile_name=AWS_PROFILE)
            credentials = session.get_credentials()
            AWS_ACCESS_KEY = credentials.access_key
            AWS_SECRET_ACCESS_KEY = credentials.secret_key
            AWS_SESSION_TOKEN = credentials.token

        cls._auth = AWSRequestsAuth(
            aws_access_key=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_token=AWS_SESSION_TOKEN,
            aws_host=cls._base_url_r53,
            aws_service='execute-api',
            aws_region=AWS_REGION
        )

        if DEBUG_HTTP:
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def _call(self, _method, _invoke_url_r53=None, _auth=None, _data=None, params=None):

        # allow overridding the auth
        auth = self._auth
        if _auth is not None:
            auth = _auth

        if _invoke_url_r53 is None:
            _invoke_url_r53 = self._invoke_url_r53

        response = requests.request(
            method=_method,
            url=_invoke_url_r53,
            params=params,
            auth=auth,
            data=_data,
            verify=f'{os.getcwd()}/tests/route_53/swadevrootca1.pem'
        )
        return response

    def _validate_response(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code)

    @pytest.fixture(scope='class')
    def setup_artifact_for_testing(self, request):

        stack_name = "Describe-Artifact-R53-E2E-Test"
        artifact_key = "/test/route53/artifact.zip"
        deployment_selector = "dev"
        aws_region = "us-east-1"

        arn = f'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/{stack_name}/dev'

        _data = json.dumps({
            "stack_name": stack_name,
            "artifact_key": artifact_key,
            "owner_account_id": "1234567890",
            "deployment_selector": deployment_selector,
            "aws_region": aws_region
        })
        response = self._generate_presigned_url(_data)
        assert 200 == response.status_code
        with open("./tests/deployment_packages/landing-zone-integration-test-artifact/LandingZoneTest.zip", 'rb') as fd:
            self._upload_deployment_package(fd, json.loads(response.text))
        yield
        # delete artifact here, when delete method is implemented
        self.delete_artifact(arn)

    def _generate_presigned_url(self, _data):
        return self._call('POST', f'https://{self._base_url_r53}/registry/artifact/presigned_url', None, _data)  # noqa E501

    def _upload_deployment_package(self, fd, presigned_url_response):
        url, fields = presigned_url_response['url'], presigned_url_response['fields']
        files = {'file': fd}
        # This doesn't need the auth param, because it is using the presigned url.
        # The url includes the auth.
        response = requests.post(url, data=fields, files=files)
        assert 204 == response.status_code
        # need to pause here to make sure the updater lambda
        # has time to update the dynamodb table, otherwise
        # the test will fail.
        time.sleep(15)
        return response.headers['ETag'].strip('"')

    def describe_artifact(self, arn: str):
        ''' describe_artifact '''
        return self._call(
            'GET',
            f'https://{self._base_url_r53}/registry/artifact',
            None,
            None,
            {'arn': arn}
        )

    def delete_artifact(self, arn: str):
        ''' delete_artifact '''
        return self._call(
            'DELETE',
            f'https://{self._base_url_r53}/registry/artifact',
            None,
            None,
            {'arn': arn}
        )
