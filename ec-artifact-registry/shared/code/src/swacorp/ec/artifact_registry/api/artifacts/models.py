from dataclasses import dataclass
from typing import Optional
from swawesomo.aws.dynamodb.models import PagingParameters


@dataclass
class GetArtifactRequest:
    artifact_key: str
    version: Optional[str]


@dataclass
class GetArtifactsQueryRequest(PagingParameters):
    limit: int = 10
    ascending: bool = False


@dataclass
class GetUploadRequest:
    s3_key: str
    identity: str


@dataclass
class GetUploadStatusRequest:
    etag: str
