
import boto3
import json
import logging
import os
import time

LOGGER = logging.getLogger()
LOGGER.setLevel('INFO')

TARGET_ACCOUNT_ID = os.environ.get('TARGET_ACCOUNT_ID', None)
LOCK_TABLE_NAME = os.environ.get('LOCK_TABLE_NAME', "TerraformStateLockTable")
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', "us-east-1")
DEPLOY_ENVIRONMENT = os.environ.get('DEPLOY_ENVIRONMENT', None)

def client(service, account_id=None, cross_account_role='SWACSCloudAdmin'):
    ''' client '''
    client = boto3.client('sts', region_name=AWS_DEFAULT_REGION)
    caller_identity = client.get_caller_identity()
    LOGGER.info("caller_identity: {}".format(caller_identity))
    caller_identity_account_id = caller_identity.get('Account', None)
    if (account_id == None) or (str(caller_identity_account_id) == str(account_id)):
        '''
            if the account id was not supplied, or the account_id is the same account 
            where this lambda is running, return the default client, otherwise
            try to assume-role into the account_id
        '''
        return boto3.client(service, region_name=AWS_DEFAULT_REGION)

    # request is for another account, assume role, and return the client.
    role_arn = "arn:aws:iam::{}:role/swa/{}"\
        .format(
            account_id,
            cross_account_role
        )
    assume_role_response = client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="ec-account-registry-updater-{}"\
            .format(int(round(time.time() * 1000)))
    )
    credentials = assume_role_response.get("Credentials")
    return boto3.client(
        service,
        aws_access_key_id=credentials.get('AccessKeyId'),
        aws_secret_access_key=credentials.get('SecretAccessKey'),
        aws_session_token=credentials.get('SessionToken'),
        region_name=AWS_DEFAULT_REGION
    )


def clear_locks():
    ddb = client('dynamodb')
    result = ddb.scan(
        TableName=LOCK_TABLE_NAME,
        Select='ALL_ATTRIBUTES',
        FilterExpression='contains(LockID, :workspace)',
        ExpressionAttributeValues={
            ":workspace": {
                "S": DEPLOY_ENVIRONMENT
            }
        }
    )
    for lock in result['Items']:
        print("lock: {}".format(lock))
        lock_id = lock['LockID']['S']
        # print("deleting lock: {} ".format(lock_id))
        delete_result = ddb.delete_item(
            Key={
                'LockID': {
                    'S': lock_id
                }
            },
            TableName=LOCK_TABLE_NAME
        )
        print("delete_result: {}".format(delete_result['ResponseMetadata']))
        # print("delete_result: {}".format(delete_result['ResponseMetadata']['HTTPSStatusCode']))

if __name__ == '__main__':
    print("TARGET_ACCOUNT_ID: {}".format(TARGET_ACCOUNT_ID))
    print("LOCK_TABLE_NAME: {}".format(LOCK_TABLE_NAME))
    print("AWS_DEFAULT_REGION: {}".format(AWS_DEFAULT_REGION))
    print("DEPLOY_ENVIRONMENT: {}".format(DEPLOY_ENVIRONMENT))
    clear_locks()
