
import boto3
import json
import pytest
import re
import requests
import time

from contextlib import closing
from tests import AWS_REGION, BaseTestCase, DEPLOY_ENVIRONMENT

class BaseLambdaTestCase(BaseTestCase):
    '''BaseLambdaTestCase
    Common methods and resources for Lambda-Based Tests
    '''

    @classmethod
    def setUpClass(cls):
        ''' setUpClass '''
        deploy_environment = re.sub(
            r'\.',
            '-',
            DEPLOY_ENVIRONMENT
        )

        cls._get_presigned_url_function_name = f'new_account_artifact_registry-{deploy_environment}'
        cls._generate_deployment_plan_function_name = f'new_account_artifact_registry-{deploy_environment}'
        cls._describe_artifact_function_name = f'new_account_artifact_registry-{deploy_environment}'

    def _call(self, _data, _function_name):
        client = boto3.client('lambda', AWS_REGION)
        response = client.invoke(
            FunctionName=_function_name,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=bytes(_data, 'utf8')
        )
        return response

    def generate_presigned_url(self, presigned_url_request):
        response = self._call(presigned_url_request, self._get_presigned_url_function_name)
        assert response['StatusCode'] == 200
        _payload = response['Payload']
        payload = json.loads(_payload.read().decode('utf8'))
        assert payload['statusCode'] == 200
        return payload

    def upload_deployment_package(self, fd, presigned_url_response):
        url, fields = presigned_url_response['url'], presigned_url_response['fields']
        files = {'file': fd}
        # This doesn't need the auth param, because it is using the presigned url.
        # The url includes the auth.
        response = requests.post(url, data=fields, files=files)
        assert 204 == response.status_code
        time.sleep(10)
        return response.headers['ETag'].strip('"')

    @pytest.fixture(scope='class')
    def setup_artifact_for_testing(self, request):

        arn = 'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Describe-Artifact-E2E-Test/dev'

        stack_name = "Describe-Artifact-E2E-Test"
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
        yield
        # delete artifact after testing is finished
        delete_artifact_response = self.delete_artifact(arn)
        assert 201 == delete_artifact_response['statusCode']

    def describe_artifact(self, arn: str):
        _data = json.dumps({
            "resource": "/registry/artifact",
            "path": "/registry/artifact",
            "queryStringParameters": {
                "arn": arn
            },
            "httpMethod": "GET",
            "isBase64Encoded": False
        })
        response = self._call(_data, self._describe_artifact_function_name)
        return json.loads(response['Payload'].read().decode('utf8'))

    def delete_artifact(self, arn: str):
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
        return json.loads(response['Payload'].read().decode('utf8'))
