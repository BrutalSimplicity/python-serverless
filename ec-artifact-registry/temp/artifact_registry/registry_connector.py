import logging
from boto3.dynamodb.conditions import Key, Attr
from shared.artifact_registry.exceptions import ArtifactNotFoundError
from functools import partial
from typing import List, NamedTuple, Optional, Any, Mapping
from swawesomo.common.optional import OptionalHandler as opt
from shared.connector import Connector
from swawesomo.common.logging import log_it
from shared.artifact_registry.models import (
    ListArtifactsRequest,
    PagingParameters
)

log_it_p1 = partial(log_it, level=logging.INFO)

STACK_NAME_PREFIX = 'stack-name'
OWNER_ACCOUNT_ID_PREFIX = 'owner-account-id'

class ArtifactRegistryEntity(NamedTuple):
    stack_name: str
    artifact_key: str
    version_id: str
    owner_account_id: str
    dependent_artifacts: Optional[List[str]]
    deployment_selector: str
    manifest_template: str
    aws_region: str
    arn: str

    @classmethod
    def create(cls, dynamodb_item):
        return ArtifactRegistryEntity(
            stack_name=dynamodb_item['StackName'],
            artifact_key=dynamodb_item['ArtifactKey'],
            version_id=dynamodb_item['VersionId'],
            owner_account_id=dynamodb_item['OwnerAccountId'],
            dependent_artifacts=opt(dynamodb_item)['DependentArtifacts'].value(),
            deployment_selector=dynamodb_item['DeploymentSelector'],
            manifest_template=dynamodb_item['ManifestTemplate'],
            aws_region=dynamodb_item['AwsRegion'],
            arn=dynamodb_item['Arn'],
        )

    def to_dynamodb_item(self):
        return {
            'ArtifactKey': self.artifact_key,
            'StackName': self.stack_name,
            'VersionId': self.version_id,
            'OwnerAccountId': self.owner_account_id,
            'DependentArtifacts': self.dependent_artifacts,
            'DeploymentSelector': self.deployment_selector,
            'ManifestTemplate': self.manifest_template,
            'AwsRegion': self.aws_region,
            'Arn': self.arn
        }

class ArtifactCollecionEntity(NamedTuple):
    items: List[ArtifactRegistryEntity]
    last_evaluated_key: None

class ArtifactRegsitryConnector(Connector):

    def __init__(self, dynamodb, table_name: str):
        super().__init__(dynamodb, table_name)

    def save_artifact(self, entity: ArtifactRegistryEntity):
        dynamodb_item = entity.to_dynamodb_item()
        self.table.put_item(Item=dynamodb_item)

    def describe_artifact(self, arn: str):
        key_condition = Key('Arn').eq(arn)
        entities = self._make_scan(key_condition)

        # should only be one artifact
        if len(entities) == 1:
            return ArtifactRegistryEntity.create(entities[0])
        elif len(entities) == 0:
            # if none found, raise ArtifactNotFound
            raise ArtifactNotFoundError(
                f'Artifact with arn [{arn}] was not found.'
            )

        # not sure what to do here if there are more than one.

    def delete_artifact(self, arn: str, owner_account_id: str):
        self._make_delete(arn, owner_account_id)

    def list_artifacts(self, request: ListArtifactsRequest, paging: PagingParameters):
        entities = []
        last_evaluated_key: None

        if request.is_empty_request():
            entities, last_evaluated_key = self._make_paging_scan(None, paging)
        else:
            filtered_items = request.get_filtered_items()
            item = filtered_items.pop()
            condition = Attr(list(item.keys())[0]).eq(list(item.values())[0])
            entities, last_evaluated_key = self._make_paging_scan(condition, paging)

        return ArtifactCollecionEntity(
            items=[ArtifactRegistryEntity.create(entity) for entity in entities],
            last_evaluated_key=last_evaluated_key
        )
