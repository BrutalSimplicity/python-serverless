import os
from typing import Any, Callable, Optional, TypeVar, Union
from swawesomo.common.logging import log_it as _log_it
import logging

LOGGER_KEY = "swacorp.ec.artifact_registry.logger"
LOGGER = logging.getLogger(LOGGER_KEY)
LOGGER.setLevel(logging.WARNING)
LOGGER.warning(f"{LOGGER_KEY}: has been added")

F = TypeVar("F", bound=Callable[..., Any])


def log_it(level=LOGGER.level, only_on_error=False) -> Callable[[F], F]:
    return _log_it(level=level, only_on_error=only_on_error, logger=LOGGER)  # type: ignore


def set_log_level(level: Optional[Union[str, int]] = None):
    level = (
        level
        or os.environ.get("LOG_LEVEL", "").upper()
        or os.environ.get("LOGLEVEL", "").upper()
        or logging.WARNING
    )
    LOGGER.setLevel(level)
