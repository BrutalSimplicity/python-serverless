
import base64
from swawesomo.common.json import decoder, encoder
from typing import Any, List, Mapping, NamedTuple, Optional, Type, Union
from dataclasses import dataclass


class ArtifactEntity(NamedTuple):
    arn: str
    artifact_key: str
    dependent_artifacts: List[str]
    deployment_selector: str
    manifest_template: Mapping[str, str]
    owner_account_id: str
    stack_name: str
    version: str

    @classmethod
    def create(cls, dynamodb_item):
        return ArtifactEntity(
            arn=dynamodb_item['Arn'],
            artifact_key=dynamodb_item['ArtifactKey'],
            dependent_artifacts=dynamodb_item['DependentArtifacts'],
            deployment_selector=dynamodb_item['DeploymentSelector'],
            manifest_template=dynamodb_item['ManifestTemplate'],
            owner_account_id=dynamodb_item['OwnerAccountId'],
            stack_name=dynamodb_item['StackName'],
            version=dynamodb_item['VersionId']
        )

    def to_dynamodb_item(self):
        return {
            'Arn': self.arn,
            'ArtifactKey': self.artifact_key,
            'Region': self.aws_region,
            'DependentArtifacts': self.dependent_artifacts,
            'DeploymentSelector': self.deployment_selector,
            'ManifestTemplate': self.manifest_template,
            'OwnerAccountId': self.owner_account_id,
            'StackName': self.stack_name,
            'VersionId': self.version
        }

class PagingParameters(NamedTuple):
    limit: int
    ascending: bool
    last_evaluated_key: Optional[Mapping[str, Any]] = None

class PresignedURLRequestBody(NamedTuple):
    '''
        Represents the body parameter for an API Gateway PresignedURL Request
    '''
    stack_name: str
    artifact_key: str
    owner_account_id: str
    deployment_selector: str
    aws_region: str
    dependent_artifacts: Any = []

@dataclass
class PresignedURLRequest:
    '''
        Represents an API Gateway PresignedURL Request.

        The `body` of the API Request is used to populated this Object
    '''
    resource: str
    path: str
    httpMethod: str
    body: Union[str, PresignedURLRequestBody]
    isBase64Encoded: bool
    headers: Any = None
    multiValueHeaders: Any = None
    queryStringParameters: Any = None
    multiValueQueryStringParameters: Any = None
    pathParameters: Any = None
    stageVariables: Any = None
    requestContext: Any = None

    def get_body(self) -> PresignedURLRequestBody:
        body = self.body
        if isinstance(body, str):
            body = decoder(body)
        return PresignedURLRequestBody(**body._asdict())

    def build_presigned_url_meta(self) -> str:
        '''
            Builds the Metadata String that is passed back during the
            presigned url request.

            - artifact_key
            - stack-name
            - owner-account-id
            - deployment-selector
            - aws_region
            - dependent-artifacts
        '''
        body = self.get_body()
        response = {
            "artifact_key": body.artifact_key,
            "stack_name": body.stack_name,
            "owner_account_id": body.owner_account_id,
            "deployment_selector": body.deployment_selector,
            "aws_region": body.aws_region
        }

        if body.dependent_artifacts is not None:
            response['dependent_artifacts'] = body.dependent_artifacts

        return base64.urlsafe_b64encode(
            bytes(encoder(response), 'utf-8')
        ).decode('utf-8')

    def build_arn(self) -> str:
        body = self.get_body()
        return f'arn:aws:ec-artifact-registry:{body.aws_region}:{body.owner_account_id}:artifact/{body.stack_name}/{body.deployment_selector}'  # noqa E501

class GenerateDeploymentPlanRequest(NamedTuple):
    ''' Request to Generate a Deployment Plan '''
    deployment_selector: str

class DescribeArtifactRequest(NamedTuple):
    ''' Request to retrieve details about an Artifact '''
    arn: str

@dataclass
class DeleteArtifactRequest:
    arn: str
    deployment_selector: str

@dataclass
class ListArtifactsRequest(NamedTuple):
    deployment_selector: str
    org: str

class DeploymentPlan(NamedTuple):
    ''' Represents a Generated Deployment Plan '''
    root_artifacts: List[str] = []
    stem_artifacts: List[str] = []
    leaf_artifacts: List[str] = []

class Object(NamedTuple):
    key: str
    size: int
    eTag: str
    versionId: str
    sequencer: str

class Bucket(NamedTuple):
    name: str
    ownerIdentity: Any
    arn: str

class S3(NamedTuple):
    s3SchemaVersion: str
    configuration: str
    bucket: Type[Bucket]
    object: Type[Object]

class Record(NamedTuple):
    '''
        Represents the S3 Event Record
    '''
    eventVersion: str
    eventSource: str
    awsRegion: str
    eventTime: str
    eventName: str
    userIdentity: Any
    requestParameters: Any
    responseElements: Any
    s3: Type[S3]

class RegsitryArtifactModel(NamedTuple):
    ''' S3 ArtifactRegistry Object '''
    bucket: str
    artifact_key: str
    version_id: str
