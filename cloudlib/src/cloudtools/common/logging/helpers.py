import logging
import os
from typing import Optional, Union

def set_log_level(level: Optional[Union[str, int]] = None):
    '''Set the log level for the root logger.

    This is a helper method to set the logging level for the root
    logger based on manual input, environment variables (LOGLEVEL, LOG_LEVEL),
    or a default.

    Args:
        level:  Logging level to be set. Defaults to `logging.WARNING` if
                if not set and no environment variables are found.
    '''
    level = (
        level
        or os.environ.get('LOG_LEVEL', '').upper()
        or os.environ.get('LOGLEVEL', '').upper()
        or logging.WARNING
    )
    logging.getLogger().setLevel(level)
