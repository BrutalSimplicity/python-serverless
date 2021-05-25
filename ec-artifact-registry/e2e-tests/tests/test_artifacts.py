from swacorp.ec.artifact_registry.api.artifacts.resources import get_upload_status
import boto3
from swacorp.ec.artifact_registry.api.artifacts.models import (
    GetArtifactRequest,
    GetUploadRequest,
)
from swacorp.ec.artifact_registry.api.client import ApiClient
from swacorp.ec.artifact_registry.api.session import SessionParams
import pytest


@pytest.fixture
def client():
    return ApiClient(
        SessionParams(
            boto3.Session(),
            endpoint="https://krt.api.krt.registry.ec.dev.aws.swacorp.com",
        )
    )


@pytest.fixture
def get_not_found_artifact():
    return GetArtifactRequest("somekey", "some_version")


@pytest.fixture
def get_upload_presigned_url():
    return GetUploadRequest("test", "me")


def test_get_not_found_artifact(client: ApiClient, get_not_found_artifact):
    response = client.get_artifact(get_not_found_artifact)
    assert "statusCode" in response
    assert response["statusCode"] == 404


def test_get_upload_presigned_url(
    client: ApiClient, get_upload_presigned_url: GetUploadRequest
):
    response = client.upload(get_upload_presigned_url.s3_key)
    assert "statusCode" not in response
