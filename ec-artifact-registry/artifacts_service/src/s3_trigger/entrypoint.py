import logging

from s3_trigger.handlers.artifacts import handler as artifacts_handler
from s3_trigger.handlers.exceptions import exceptions_handler
from swacorp.ec.artifact_registry.aws.models import S3EventModel
from swacorp.ec.artifact_registry.logging import log_it, set_log_level
from swawesomo.common.logging.logging_context import use_logging_context
from swawesomo.common.utils import response_asdict

set_log_level()


@response_asdict
@use_logging_context
@log_it(level=logging.INFO)
def lambda_handler(event, context):
    try:
        model = S3EventModel.create(event)
        response = artifacts_handler(model)
        return response
    except Exception as ex:
        return exceptions_handler(ex)
