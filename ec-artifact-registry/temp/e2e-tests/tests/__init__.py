import boto3
import os
import sys
import requests
import unittest
import logging

from aws_requests_auth.aws_auth import AWSRequestsAuth

sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '.', 'shared'))

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
aws_region_short_dict = {
    'us-east-1': 'awsuse1',
    'us-west-2': 'awsusw2'
}
aws_region_short = aws_region_short_dict.get(AWS_REGION)

if DEBUG_HTTP:
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

class BaseTestCase(unittest.TestCase):

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

        if AWS_PROFILE is not None:
            # retrieve credentials using a profile
            session = boto3.session.Session(profile_name=AWS_PROFILE)
            credentials = session.get_credentials()
            AWS_ACCESS_KEY = credentials.access_key
            AWS_SECRET_ACCESS_KEY = credentials.secret_key
            AWS_SESSION_TOKEN = credentials.token

        # auth used for requests via Route53
        cls.auth_r53 = AWSRequestsAuth(
            aws_access_key=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_token=AWS_SESSION_TOKEN,
            aws_host=cls.base_url,
            aws_service='execute-api',
            aws_region=AWS_REGION
        )

        # auth used for requests via API Gateway
        cls._auth = AWSRequestsAuth(
            aws_access_key=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_token=AWS_SESSION_TOKEN,
            aws_host=cls.base_url,
            aws_service='execute-api',
            aws_region=AWS_REGION
        )

        if DEBUG_HTTP:
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def _call(self, _method, _url, _auth, _data):
        auth = self._auth
        if _auth is None:
            auth = _auth
        response = requests.request(
            method=_method,
            url=_url,
            auth=auth,
            verify=False,
            data=_data
        )
        return response

    def _validate_response(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code)
