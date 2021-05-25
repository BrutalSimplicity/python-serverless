import logging

from api.handlers.exceptions import exceptions_handler
from swacorp.ec.artifact_registry.aws.models import ApiGatewayEventModel
from swawesomo.common.logging import log_it
from swawesomo.common.logging.helpers import set_log_level
from swawesomo.common.logging.logging_context import use_logging_context
from swawesomo.common.utils import response_asdict

from .handlers.deployments import handler as deployments_handler

set_log_level()


@response_asdict
@use_logging_context
@log_it(level=logging.INFO)
def lambda_handler(event, context):
    try:
        model = ApiGatewayEventModel.create(event)
        response = deployments_handler(model)
        return response
    except Exception as ex:
        return exceptions_handler(ex)
