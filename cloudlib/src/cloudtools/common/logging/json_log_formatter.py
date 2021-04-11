import logging
import sys
from datetime import datetime
from logging import StreamHandler

from cloudtools.common.json import encoder


class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        if isinstance(record.msg, str):
            message = super().format(record)
            return encoder({
                'message': message,
                'timestamp': datetime.utcfromtimestamp(record.created).strftime('%y-%m-%dT%h:%M%S'),
                'level': record.levelname
            })
        else:
            return encoder(record.msg)


def add_json_handler(logger: logging.Logger):
    handler = StreamHandler(sys.stderr)
    handler.setFormatter(JsonLogFormatter())
    logger.handlers.insert(1, handler)
