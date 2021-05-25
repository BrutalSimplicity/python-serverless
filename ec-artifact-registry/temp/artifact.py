from functools import partial
import logging
import os
import uuid
import zipfile
from dataclasses import dataclass, asdict
from io import BytesIO

from shared.artifact_registry.models import RegsitryArtifactModel
from shared.exceptions import BaseHttpFormattedError
from shared.logging import log_it

log_it_p1 = partial(log_it, level=logging.INFO)

class ArtifactIsNotAZipError(BaseHttpFormattedError):
    fmt = 'ArtifactRegistry artifact is not a zipfile: {}'

@dataclass
class ArtifactBufferResult:
    artifact: RegsitryArtifactModel
    metadata: dict
    artifact_buffer: BytesIO

@dataclass
class ExtractArtifactResult(ArtifactBufferResult):
    local_artifact_path: str

def get_artifact_buffer(s3, request: RegsitryArtifactModel):
    input_artifact = s3.get_object(
        Bucket=request.bucket,
        Key=request.artifact_key,
        VersionId=request.version_id
    )
    return ArtifactBufferResult(
        request,
        input_artifact["Metadata"],
        BytesIO(input_artifact["Body"].read())
    )

@log_it_p1
def generate_local_dir_name_for_artifact():
    local_artfact_dir = uuid.uuid4()
    local_artifact_path = "/tmp/{}".format(local_artfact_dir)
    return local_artifact_path

def extract_artifact_to_local_filesystem(data: ArtifactBufferResult):
    artifact_buffer = data.artifact_buffer
    artifact: RegsitryArtifactModel = data.artifact

    @log_it_p1
    def is_valid_zip_file(artifact_key):
        return zipfile.is_zipfile(artifact_buffer)

    @log_it_p1
    def extract():
        if not is_valid_zip_file(artifact.artifact_key):
            raise ArtifactIsNotAZipError(artifact.artifact_key)

        local_artifact_path = generate_local_dir_name_for_artifact()

        zipfile.ZipFile(artifact_buffer).extractall(local_artifact_path)

        return {
            'local_artifact_path': local_artifact_path,
            'local_artifact_path:listdir': os.listdir(local_artifact_path)
        }

    result = extract()

    return ExtractArtifactResult(local_artifact_path=result['local_artifact_path'],
                                 **asdict(data))
