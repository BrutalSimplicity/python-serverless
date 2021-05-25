from swacorp.ec.artifact_registry.artifacts.models import ArtifactUploadStatusEntity
from swacorp.ec.artifact_registry.exceptions import (
    ErrorResponseModel,
)
from s3_trigger.data import artifacts_connector
from swacorp.ec.artifact_registry.logging import log_it
from swacorp.ec.artifact_registry.aws.models import S3EventModel


@log_it(only_on_error=True)
def exceptions_handler(ex: Exception):
    return ErrorResponseModel.create(ex)


def artifacts_handler(model: S3EventModel, ex: Exception):
    return
