import os
from typing import cast

import boto3
from botocore.config import Config
from swacorp.ec.artifact_registry.artifacts.connector import ArtifactsConnnector
from swawesomo.common.lazy import Lazy

ARTIFACTS_REGISTRY_TABLE = os.environ["ARTIFACTS_REGISTRY_TABLE"]

artifacts_connector = Lazy(
    lambda: ArtifactsConnnector(boto3.resource("dynamodb"), ARTIFACTS_REGISTRY_TABLE)
).cast()
