import logging
from boto3.dynamodb.conditions import Key
from dataclasses import dataclass
from typing import ClassVar, Literal, Optional, Tuple

from swacorp.ec.artifact_registry.aws.dynamodb.models import (
    DynamoDBEntity,
    DynamoDBQuery,
    KeyGenerator,
)
from swacorp.ec.artifact_registry.artifacts.models import (
    ArtifactEntity,
    ArtifactUploadStatusEntity,
)
from swacorp.ec.artifact_registry.logging import LOGGER, log_it
from swawesomo.aws.dynamodb.dynamodb_connector import DynamodbConnector
from swawesomo.aws.dynamodb.models import PagingParameters
from swawesomo.common.utils import generate_timestamp
from swawesomo.common.models.mapping import from_dict

PARTITION_KEY = "PK"
SORT_KEY = "SK"
GSI1PK = "GSI1PK"
GSI1SK = "GSI1SK"


@dataclass
class ArtifactUploadStatusEntityDocument(DynamoDBEntity, ArtifactUploadStatusEntity):
    __prefix__: ClassVar[str] = "artifact_status"
    key_gen: ClassVar[KeyGenerator] = KeyGenerator(__prefix__)

    @classmethod
    def create(cls, entity: ArtifactUploadStatusEntity):
        return ArtifactUploadStatusEntityDocument(
            PK=cls.key_gen.generate(entity.artifact_key),
            SK=cls.key_gen.generate(entity.etag),
            GSI1PK=None,
            GSI1SK=None,
            etag=entity.etag,
            status=entity.status,
            artifact_key=entity.artifact_key,
            error=entity.error,
        )

    @classmethod
    @log_it(level=logging.DEBUG)
    def create_get(cls, etag: str, artifact_key: Optional[str] = None):
        return DynamoDBEntity(
            PK=cls.key_gen.generate(artifact_key),
            SK=cls.key_gen.generate(etag),
            GSI1PK=None,
            GSI1SK=None,
        )


@dataclass
class ArtifactEntityDocument(DynamoDBEntity, ArtifactEntity):
    __prefix__: ClassVar[str] = "artifact"
    key_gen: ClassVar[KeyGenerator] = KeyGenerator(__prefix__)

    @classmethod
    def create(cls, entity: ArtifactEntity):
        return ArtifactEntityDocument(
            PK=cls.key_gen.generate(entity.artifact_key),
            SK=cls.key_gen.generate(entity.timestamp),
            GSI1PK=cls.key_gen.generate(entity.artifact_key),
            GSI1SK=cls.key_gen.generate(entity.version),
            artifact_key=entity.artifact_key,
            stack_name=entity.stack_name,
            version=entity.version,
            etag=entity.etag,
            timestamp=generate_timestamp(),
            manifest=entity.manifest,
            metadata=entity.metadata,
        )

    @classmethod
    @log_it(level=logging.DEBUG)
    def create_query(
        cls,
        artifact_key: Optional[str],
        condition: Optional[Tuple[Literal["version", "timestamp"], str]],
        paging: PagingParameters,
    ):
        if not condition:
            return DynamoDBQuery(
                key_condition=DynamoDBEntity.PartitionKey().eq(
                    cls.key_gen.generate(artifact_key)
                ),
                paging=paging,
            )
        if condition[0] == "timestamp":
            return DynamoDBQuery(
                key_condition=DynamoDBEntity.PartitionKey().eq(
                    cls.key_gen.generate(artifact_key)
                )
                & Key("SK").begins_with(cls.key_gen.generate(condition[1])),
                paging=paging,
            )
        return DynamoDBQuery(
            key_condition=DynamoDBEntity.GlobalSecondaryIndexOnePartitionKey().eq(
                cls.key_gen.generate(artifact_key)
            )
            & DynamoDBEntity.GlobalSecondaryIndexOneSortKey().eq(
                cls.key_gen.generate(condition[1])
            ),
            index=DynamoDBEntity.GlobalSecondaryIndexOne(),
            paging=paging,
        )


class ArtifactsConnnector(DynamodbConnector):
    def __init__(self, dynamodb, table_name: str):
        super().__init__(dynamodb, table_name)
        self.dynamodb = dynamodb
        self.table = self.dynamodb.Table(table_name)

    def save_artifact(self, artifact: ArtifactEntity):
        document = ArtifactEntityDocument.create(artifact)
        self.table.put_item(Item=document.to_dict())

    def save_upload_status(self, status: ArtifactUploadStatusEntity):
        document = ArtifactUploadStatusEntityDocument.create(status)
        self.table.put_item(Item=document.to_dict())

    @log_it(level=logging.DEBUG)
    def query_artifacts(
        self,
        artifact_key: Optional[str],
        version: Optional[str],
        paging: PagingParameters,
    ):
        condition = ("version", version) if version else None
        query = ArtifactEntityDocument.create_query(artifact_key, condition, paging)
        return self._make_query(
            key_condition=query.key_condition,
            paging=query.paging,
            index=query.index,
            mapper=lambda e: from_dict(ArtifactEntity, e),
        )

    @log_it(level=logging.DEBUG)
    def get_upload_status(self, etag: str):
        get_item = ArtifactUploadStatusEntityDocument.create_get(etag)
        result = self.table.get_item(Key=get_item.to_key())
        if "Item" in result:
            return from_dict(ArtifactUploadStatusEntity, result)
        return None
