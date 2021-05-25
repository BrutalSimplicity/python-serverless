import os

import boto3
from swacorp.ec.artifact_registry.artifacts.connector import ArtifactsConnnector
from swawesomo.common.lazy import Lazy

ARTIFACTS_REGISTRY_BUCKET = Lazy(lambda: os.environ["ARTIFACTS_REGISTRY_BUCKET"])
s3 = Lazy(lambda: boto3.client("s3")).cast()
ARTIFACTS_REGISTRY_TABLE = os.environ["ARTIFACTS_REGISTRY_TABLE"]
artifacts_connector = Lazy(
    lambda: ArtifactsConnnector(boto3.resource("dynamodb"), ARTIFACTS_REGISTRY_TABLE)
).cast()
