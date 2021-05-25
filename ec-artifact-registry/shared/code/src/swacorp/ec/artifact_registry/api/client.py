from swacorp.ec.artifact_registry.api.artifacts.models import (
    GetArtifactRequest,
    GetUploadStatusRequest,
)
from swacorp.ec.artifact_registry.api.artifacts.resources import (
    get_artifact,
    get_artifacts,
    get_upload_status,
    upload,
)
from swacorp.ec.artifact_registry.api.session import SessionParams
from swawesomo.aws.dynamodb.models import PagingParameters
from swawesomo.common.logging.helpers import set_log_level

set_log_level()


def artifacts_route(resource: str):
    return "/".join(["artifacts", resource])


def deployment_plans_route(resource: str):
    return "/".join(["deployments/plans", resource])


def deployemnts_route(resource: str):
    return "/".join(["deployments", resource])


class ApiClient:
    def __init__(self, params: SessionParams):
        self._session = params

    def get_artifact(self, request: GetArtifactRequest):
        return get_artifact(self._session, request)

    def get_artifacts(self, paging: PagingParameters):
        return get_artifacts(self._session, paging)

    def upload(self, s3_key: str):
        return upload(self._session, s3_key)

    def get_upload_status(self, request: GetUploadStatusRequest):
        return get_upload_status(self._session, request)
