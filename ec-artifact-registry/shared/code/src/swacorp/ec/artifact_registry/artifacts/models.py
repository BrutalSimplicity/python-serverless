from dataclasses import dataclass
import enum
from typing import Any, List, Mapping, Optional, Union


@dataclass
class ArtifactEntity:
    artifact_key: str
    stack_name: str
    version: str
    etag: str
    timestamp: str
    manifest: Mapping[str, Any]
    metadata: Optional[Mapping[str, Any]]


@dataclass
class ArtifactUploadStatusErrorEntity:
    message: str
    stack_trace: Optional[List[str]]


class ArtifactUploadStatus(str, enum.Enum):
    PROCESSING = "PROCESSING"
    OK = "OK"
    FAIL = "FAIL"


@dataclass
class ArtifactUploadStatusEntity:
    etag: str
    status: ArtifactUploadStatus
    artifact_key: Optional[str]
    error: Optional[ArtifactUploadStatusErrorEntity]
