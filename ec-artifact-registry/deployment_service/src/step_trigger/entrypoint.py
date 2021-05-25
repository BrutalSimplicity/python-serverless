import logging
from swawesomo.common.logging import log_it, use_logging_context


@use_logging_context
@log_it(level=logging.INFO)
def lambda_handler(event, context):
    return event
