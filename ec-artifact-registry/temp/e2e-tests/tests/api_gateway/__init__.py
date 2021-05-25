
import boto3
import json
import pytest
import requests
import os
import re
import sys
import time

from aws_requests_auth.aws_auth import AWSRequestsAuth
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
from contextlib import closing
from ..shared.aws.apigw import lookup_apigw_id, lookup_apigw_id_paginator
from tests import (
    AWS_PROFILE,
    AWS_ACCESS_KEY,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN,
    AWS_REGION,
    AWS_ACCOUNT_ID,
    BaseTestCase,
    DEPLOY_ENVIRONMENT,
)

sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '.', 'shared'))

STACK_NAME = "Describe-Artifact-E2E-API-Gateway-Test"

class BaseAPIGatewayTestCase(BaseTestCase):
    '''BaseAPIGatewayTestCase
        Common methods and resources for API Gateway-Based Tests
    '''

    @classmethod
    def setUpClass(cls) -> None:
        ''' setUpClass '''
        global AWS_ACCOUNT_ID
        global AWS_ACCESS_KEY
        global AWS_SECRET_ACCESS_KEY
        global AWS_SESSION_TOKEN
        global AWS_REGION
        global AWS_PROFILE
        global STACK_NAME
        global DEPLOY_ENVIRONMENT
        APIGW_NAME = f'ECArtifactRegistry-{DEPLOY_ENVIRONMENT}'
        cls._apigw_id = lookup_apigw_id_paginator(APIGW_NAME)
        if cls._apigw_id is None:
            raise Exception(f'API Gateway with name [{APIGW_NAME}] was not found.  Can\'t test an API that cannot be found.')  # noqa E501
        cls._base_url = f'{cls._apigw_id}.execute-api.{AWS_REGION}.amazonaws.com'
        deploy_environment = re.sub(
            r'\.',
            '-',
            DEPLOY_ENVIRONMENT
        ).lower()
        cls._deploy_environment = deploy_environment
        cls._invoke_url_base = f'https://{cls._base_url}/{deploy_environment}'
        cls._invoke_url = f'https://{cls._base_url}/{deploy_environment}/registry/artifact'

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
            aws_host=cls._base_url,
            aws_service='execute-api',
            aws_region=AWS_REGION
        )

        cls._boto_auth = BotoAWSRequestsAuth(
            aws_host=cls._base_url,
            aws_service='execute-api',
            aws_region=AWS_REGION
        )

    def _call(self, _method, _invoke_url=None, auth=None, _data=None, params=None):
        if _invoke_url is None:
            _invoke_url = self._invoke_url

        if auth is None:
            auth = self._boto_auth

        response = requests.request(
            method=_method,
            url=_invoke_url,
            params=params,
            auth=auth,
            verify=True,
            data=_data
        )
        return response

    @pytest.fixture(scope='class')
    def setup_artifact_for_testing(self, request):
        arn = f'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/{STACK_NAME}/dev'

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
        with closing(open("./tests/deployment_packages/landing-zone-integration-test-artifact/LandingZoneTest.zip", 'rb')) as fd:
            self._upload_deployment_package(fd, json.loads(response.text))

        yield

        # delete artifact when the test is done
        self.delete_artifact(arn)

    def _generate_presigned_url(self, _data):
        return self._call('POST', f'{self._invoke_url_base}/registry/artifact/presigned_url', None, _data)  # noqa E501

    def _upload_deployment_package(self, fd, presigned_url_response):
        url, fields = presigned_url_response['url'], presigned_url_response['fields']
        files = {'file': fd}
        # This doesn't need the auth param, because it is using the presigned url.
        # The url includes the auth.
        response = requests.post(url, data=fields, files=files)
        assert 204 == response.status_code
        time.sleep(10)
        return response.headers['ETag'].strip('"')

    def describe_artifact(self, arn: str):
        ''' describe_artifact '''
        return self._call(
            'GET',
            f'{self._invoke_url_base}/registry/artifact',
            None,
            None,
            {'arn': arn}
        )

    def delete_artifact(self, arn: str):
        ''' delete_artifact '''
        return self._call(
            'DELETE',
            f'{self._invoke_url_base}/registry/artifact',
            None,
            None,
            {'arn': arn}
        )
