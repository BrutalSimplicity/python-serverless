import traceback
from dataclasses import dataclass
from typing import List
from swawesomo.common.errors import BaseFormattedError


@dataclass
class ErrorResponseModel:
    status_code: str
    message: str
    stack_trace: List[str]

    @classmethod
    def create(cls, ex: Exception):
        if isinstance(ex, BaseFormattedError):
            return ErrorResponseModel(
                status_code=str(ex.status_code),
                message=str(ex),
                stack_trace=traceback.format_tb(ex.__traceback__),
            )


class NotFoundException(BaseFormattedError):
    fmt = "The resource was not found"

    def __init__(self):
        super().__init__()
        self.status_code: int = 404
