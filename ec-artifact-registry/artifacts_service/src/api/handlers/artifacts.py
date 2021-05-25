import logging
import os
import boto3
from botocore.config import Config
from api.data import artifacts_connector
from swacorp.ec.artifact_registry.api.artifacts.models import (
    GetArtifactRequest,
    GetUploadRequest,
    GetArtifactsQueryRequest,
    GetUploadStatusRequest,
)
from swacorp.ec.artifact_registry.aws.models import (
    ApiGatewayEventModel,
    ApiGatewayResponseModel,
    HttpMethod,
)
from swacorp.ec.artifact_registry.logging import log_it
from swacorp.ec.artifact_registry.mapping import from_dict
from swacorp.ec.artifact_registry.exceptions import NotFoundException
from swawesomo.common.lazy import Lazy
from swacorp.ec.artifact_registry.aws.dynamodb.models import PagingParameters

ARTIFACTS_REGISTRY_BUCKET = Lazy(lambda: os.environ["ARTIFACTS_REGISTRY_BUCKET"])
s3 = Lazy(lambda: boto3.client("s3", config=Config(signature_version="s3v4"))).cast()


def get_artifact(request: GetArtifactRequest):
    artifacts = artifacts_connector.query_artifacts(
        request.artifact_key, request.version, PagingParameters()
    ).to_list()
    if not artifacts:
        raise NotFoundException()
    return ApiGatewayResponseModel(200, artifacts[0])


def get_artifacts(request: GetArtifactsQueryRequest):
    result = artifacts_connector.query_artifacts(None, None, request)
    return ApiGatewayResponseModel(200, result)


def upload(request: GetUploadRequest):
    presigned_url = s3.generate_presigned_post(
        Bucket=ARTIFACTS_REGISTRY_BUCKET.value,
        Key=request.s3_key,
        Fields={
            "acl": "bucket-owner-full-control",
            "x-amz-server-side-encryption": "aws:kms",
            "x-amz-meta-identity": request.identity,
        },
        Conditions=[
            {"acl": "bucket-owner-full-control"},
            {"x-amz-server-side-encryption": "aws:kms"},
            {"x-amz-meta-identity": request.identity},
        ],
        ExpiresIn=3600,
    )
    return ApiGatewayResponseModel(200, presigned_url)


def get_upload_status(request: GetUploadStatusRequest):
    status = artifacts_connector.get_upload_status(request.etag)
    if not status:
        raise NotFoundException()
    return ApiGatewayResponseModel(200, status)


@log_it(level=logging.DEBUG)
def handler(event: ApiGatewayEventModel):
    if event.match_route(HttpMethod.GET, "{artifact_key}"):
        return get_artifact(from_dict(GetArtifactRequest, event.parameters))
    if event.match_route(HttpMethod.GET, ""):
        return get_artifacts(from_dict(GetArtifactsQueryRequest, event.parameters))
    if event.match_route(HttpMethod.GET, "upload"):
        return upload(
            from_dict(
                GetUploadRequest,
                {**event.query_parameters, "identity": event.identity},
            )
        )
    if event.match_route(HttpMethod.GET, "upload/status/{etag}"):
        return get_upload_status(from_dict(GetUploadStatusRequest, event.parameters))
