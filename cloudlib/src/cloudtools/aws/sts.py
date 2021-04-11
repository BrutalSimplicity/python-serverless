import boto3
import time


def create_assumed_role_session(account_id, cross_account_role=None,
                                region='us-east-1',
                                session_prefix='cloudtools-assume-role-session-'):
    client = boto3.client('sts')
    caller_identity = client.get_caller_identity()
    caller_identity_account_id = caller_identity.get('Account', None)
    if str(caller_identity_account_id) == str(account_id) and not cross_account_role:
        '''
            if the account id was not supplied, or the account_id is the same account
            where this lambda is running, return the default client, otherwise
            try to assume-role into the account_id
        '''
        return boto3.Session()

    role_arn = f"arn:aws:iam::{account_id}:role/{cross_account_role}"
    assume_role_response = client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=f'{session_prefix}-{int(round(time.time() * 1000))}'
    )
    credentials = assume_role_response.get("Credentials")
    return boto3.Session(
        aws_access_key_id=credentials.get('AccessKeyId'),
        aws_secret_access_key=credentials.get('SecretAccessKey'),
        aws_session_token=credentials.get('SessionToken'),
        region_name=region
    )


def client(service, account_id, cross_account_role, region='us-east-1'):
    ''' client '''
    session = create_assumed_role_session(account_id, cross_account_role, region=region)
    return session.client(service)
