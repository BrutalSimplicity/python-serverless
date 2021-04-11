from cloudtools.common.logging import get_logging_context

def add_general_logging_metadata(context):
    if context:
        logging_context = get_logging_context()
        if hasattr(context, 'aws_request_id'):
            logging_context.add_metadata('request_id', context.aws_request_id)
