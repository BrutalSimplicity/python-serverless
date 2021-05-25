from dataclasses import asdict
from swawesomo.aws.dynamodb.models import PagingParameters
from swacorp.ec.artifact_registry.api.artifacts.models import (
    GetArtifactRequest,
    GetUploadStatusRequest,
)
from swacorp.ec.artifact_registry.api.call import make_api_call


def route(*paths: str):
    return "/".join(["artifacts", *paths])


def get_artifact(session, request: GetArtifactRequest):
    return make_api_call(session, route(request.artifact_key))


def get_artifacts(session, paging: PagingParameters):
    return make_api_call(session, route(""), {**asdict(paging)})


def upload(session, s3_key: str):
    return make_api_call(session, route("upload"), {"s3_key": s3_key})


def get_upload_status(session, request: GetUploadStatusRequest):
    return make_api_call(session, route("upload/status", request.etag))
