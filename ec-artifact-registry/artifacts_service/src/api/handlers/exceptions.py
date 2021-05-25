from curses.ascii import isdigit
from swacorp.ec.artifact_registry.exceptions import (
    ErrorResponseModel,
)
from swawesomo.common.errors import BaseFormattedError
from swacorp.ec.artifact_registry.aws.models import ApiGatewayResponseModel
from dacite.exceptions import DaciteError
import traceback


def exceptions_handler(ex: Exception):
    if isinstance(ex, DaciteError):
        return ApiGatewayResponseModel(400, ErrorResponseModel.create(ex))
    if isinstance(ex, BaseFormattedError):
        return ApiGatewayResponseModel(
            int(ex.status_code) if isdigit(ex.status_code) else 500,
            ErrorResponseModel.create(ex),
        )
    return ApiGatewayResponseModel(
        500,
        {
            "message": str(ex),
            "stack_trace": traceback.format_tb(ex.__traceback__),
        },
    )
