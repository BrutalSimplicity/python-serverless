import requests
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

def get_authenticated_session(host: str, service: str, region: str = 'us-east-1'):
    auth = BotoAWSRequestsAuth(host, region, service)
    session = requests.Session()
    session.auth = auth

    return session
