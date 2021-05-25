import logging
from swacorp.ec.artifact_registry.artifacts.models import ArtifactUploadStatus
from swacorp.ec.artifact_registry.logging import log_it
import tempfile
from dataclasses import asdict
from pathlib import Path

from swacorp.ec.artifact_registry.artifacts.connector import (
    ArtifactEntity,
    ArtifactUploadStatusEntity,
)
from swacorp.ec.artifact_registry.aws.models import S3EventModel
from swacorp.ec.dde.manifest.package import unpack
from swawesomo.common.utils import generate_timestamp

from s3_trigger.data import artifacts_connector, s3


@log_it(level=logging.DEBUG)
def handler(model: S3EventModel):
    artifact = s3.get_object(
        Bucket=model.bucket, Key=model.key, VersionId=model.version
    )
    with tempfile.TemporaryDirectory() as tmpname:
        tmppath = Path(tmpname)
        Path(tmpname).write_bytes(artifact["Body"].read())
        package = unpack(tmppath)

    manifest = package.manifest
    stack_name = artifact_key = manifest.CloudFormation.RequestKWArgs.StackName
    artifacts_connector.save_artifact(
        ArtifactEntity(
            artifact_key=artifact_key,
            etag=model.etag,
            version=model.version,
            manifest=asdict(manifest),
            stack_name=stack_name,
            metadata=manifest.Metadata,
            timestamp=generate_timestamp(),
        )
    )
    artifacts_connector.save_upload_status(
        ArtifactUploadStatusEntity(
            etag=model.etag,
            artifact_key=artifact_key,
            status=ArtifactUploadStatus.OK,
            error=None,
        )
    )
