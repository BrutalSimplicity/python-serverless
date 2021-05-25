import base64
import boto3
import botocore
import json
import logging
import os
import traceback

from botocore.exceptions import ClientError
from botocore.client import Config

from functools import partial
from shared.json import encoder, decoder
from shared.logging import log_it

from shared.utils import generate_timestamp
from shared.aws.xray import configure_xray
from shared.optional import OptionalHandler as opt

from shared.artifact_registry.models import (
    PresignedURLRequest,
    GenerateDeploymentPlanRequest,
    DescribeArtifactRequest,
    DeleteArtifactRequest,
    ListArtifactsRequest,
    PagingParameters,
)
from shared.artifact_registry.deployment_plan_connector import DeploymentPlanConnector

from shared.artifact_registry.exceptions import ArtifactNotFoundError

from shared.artifact_registry.registry_connector import ArtifactRegsitryConnector

from shared.artifact_registry.presigned_url_validator import (
    PresignedURLRequestValidator,
)
from swawesomo.common.logging import set_log_level
from swawesomo.common.lazy import Lazy

from typing import Optional

configure_xray("new account artifact registry")
boto3.set_stream_logger("", logging.INFO)
set_log_level(logging.INFO)

ARTIFACT_REGISTRY_S3_BUCKET_NAME = os.environ["ARTIFACT_REGISTRY_S3_BUCKET_NAME"]
NEW_ACCOUNT_ARTIFACT_REGISTRY_TABLE_NAME = os.environ[
    "NEW_ACCOUNT_ARTIFACT_REGISTRY_TABLE_NAME"
]

s3 = Lazy(lambda: boto3.client("s3", config=Config(signature_version="s3v4"))).cast()
dynamodb = boto3.resource("dynamodb")
deployment_plan_connector = Lazy(
    lambda: DeploymentPlanConnector(dynamodb, NEW_ACCOUNT_ARTIFACT_REGISTRY_TABLE_NAME)
).cast()

registry_connector = Lazy(
    lambda: ArtifactRegsitryConnector(
        dynamodb, NEW_ACCOUNT_ARTIFACT_REGISTRY_TABLE_NAME
    )
).cast()


def handle_client_error(e: ClientError):
    """ handle_client_error """
    statusCode = e.response["ResponseMetadata"]["HTTPStatusCode"]
    request_id = e.response["ResponseMetadata"]["RequestId"]
    message = e.response["Error"]["Message"]
    error = {
        "statusCode": statusCode,
        "timestamp": generate_timestamp(),
        "requestId": request_id,
        "message": message,
    }
    return error


def handle_response(status_code, body):
    """ handle_response """
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": encoder(body),
        "isBase64Encoded": False,
    }


def get_event_details(event):
    resource = event.get("resource")
    path = event.get("path")
    http_method = event.get("httpMethod")
    path_parameters = event.get("pathParameters", {})
    if path_parameters is None:
        path_parameters = {}
    query_parameters = event.get("queryStringParameters", {})
    if query_parameters is None:
        query_parameters = {}
    body = event.get("body")
    return resource, path, http_method, path_parameters, query_parameters, body


def generate_presigned_post(request: PresignedURLRequest):
    presigned_url_meta = request.build_presigned_url_meta()
    artifact_key = request.get_body().artifact_key
    expiration = 3600
    presigned_url = s3.generate_presigned_post(
        Bucket=ARTIFACT_REGISTRY_S3_BUCKET_NAME,
        Key=artifact_key,
        Fields={
            "acl": "bucket-owner-full-control",
            "x-amz-server-side-encryption": "aws:kms",
            "x-amz-meta-artifact": presigned_url_meta,
        },
        Conditions=[
            {"acl": "bucket-owner-full-control"},
            {"x-amz-server-side-encryption": "aws:kms"},
            {"x-amz-meta-artifact": presigned_url_meta},
        ],
        ExpiresIn=expiration,
    )
    return handle_response(200, presigned_url)


def generate_deployment_plan(request: GenerateDeploymentPlanRequest):
    deployment_plan = deployment_plan_connector.generate_deployment_plan(request)
    return handle_response(200, deployment_plan)


def describe_artifact(request: DescribeArtifactRequest):
    try:
        entity = registry_connector.describe_artifact(request.arn)
        return handle_response(200, entity)
    except ArtifactNotFoundError as e:
        return handle_response(404, e.message)
    except botocore.exceptions.ClientError as error:
        return handle_client_error(error)


def delete_artifact(request: DeleteArtifactRequest):
    try:
        response = registry_connector.delete_artifact(
            request.arn, request.get_owner_account_id()
        )
        return handle_response(201, response)
    except ArtifactNotFoundError as e:
        return handle_response(404, e.message)
    except botocore.exceptions.ClientError as error:
        return handle_client_error(error)


def list_artifacts(request: ListArtifactsRequest, paging: PagingParameters):
    try:
        response = registry_connector.list_artifacts(request, paging)
        return handle_response(200, response)
    except botocore.exceptions.ClientError as error:
        return handle_client_error(error)


def to_paging_parameters(
    limit: int, ascending: bool, last_evaluated_key: Optional[str] = None
):
    return PagingParameters(
        limit,
        ascending,
        decoder(base64.urlsafe_b64decode(last_evaluated_key.encode()).decode())
        if last_evaluated_key
        else None,
    )


def parse_bool(value: str):
    return value.lower() in ["true", "1"] if value else False


@log_it(level=logging.INFO)
def lambda_handler(event, context):
    try:
        (
            resource,
            path,
            http_method,
            path_parameters,
            query_parameters,
            body,
        ) = get_event_details(event)

        limit = int(opt(query_parameters)["limit"].value() or 20)
        ascending = parse_bool(opt(query_parameters)["ascending"].value())
        last_evaluated_key = opt(query_parameters)["lastEvaluatedKey"].value()
        paging = to_paging_parameters(limit, ascending, last_evaluated_key)

        if path == "/registry/artifact/presigned_url":
            request = PresignedURLRequest(**event)
            validator = PresignedURLRequestValidator(request)
            errors = validator.validate()
            if len(errors) > 0:
                return handle_response(400, json.dumps(errors))
            return generate_presigned_post(request)
        elif path == "/registry/deployment_plan":
            request = GenerateDeploymentPlanRequest(**query_parameters)
            return generate_deployment_plan(request)
        elif path == "/registry/deployment_plan":
            pass
        elif path == "/registry/validate":
            pass
        elif resource == "/registry/artifacts" and http_method == "GET":
            if "deployment_selector" not in query_parameters:
                query_parameters["deployment_selector"] = None
            if "owner_account_id" not in query_parameters:
                query_parameters["owner_account_id"] = None
            request = ListArtifactsRequest(**query_parameters)
            return list_artifacts(request, paging)
        elif resource == "/registry/artifact" and http_method == "GET":
            request = DescribeArtifactRequest(**query_parameters)
            return describe_artifact(request)
        elif resource == "/registry/artifact" and http_method == "DELETE":
            request = DeleteArtifactRequest(**query_parameters)
            return delete_artifact(request)

        return handle_response(
            404,
            {
                "statusCode": 404,
                "message": f"Resource at path: {path} and http_method: {http_method} was not found.",
            },
        )
    except Exception as ex:
        if isinstance(ex, ClientError):
            error = handle_client_error(ex)
            return handle_response(error["status_code"], error)
        return handle_response(
            500,
            {
                "message": str(ex),
                "statusCcode": 500,
                "stackTrace": traceback.format_exc(),
            },
        )
