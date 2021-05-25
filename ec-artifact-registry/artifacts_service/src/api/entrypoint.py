import logging

from api.handlers.artifacts import handler as artifacts_handler
from api.handlers.default import handler as default_handler
from api.handlers.exceptions import exceptions_handler
from swacorp.ec.artifact_registry.aws.models import ApiGatewayEventModel
from swacorp.ec.artifact_registry.logging import log_it, set_log_level
from swawesomo.common.logging.logging_context import use_logging_context
from swawesomo.common.pipeline import fallback
from swawesomo.common.utils import response_asdict

set_log_level()


@response_asdict
@use_logging_context
@log_it(level=logging.INFO)
def lambda_handler(event, context):
    try:
        model = ApiGatewayEventModel.create(event)
        response = fallback(artifacts_handler, default_handler)(model)
        return response
    except Exception as ex:
        return exceptions_handler(ex)
