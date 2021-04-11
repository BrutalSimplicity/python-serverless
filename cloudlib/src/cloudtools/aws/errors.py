from dataclasses import dataclass
from cloudtools.common.optional import OptionalHandler as opt
from cloudtools.common.utils import pluck
from botocore.exceptions import ClientError

@dataclass
class ClientErrorResponse(object):
    status_code: int
    error_code: str
    message: str

def client_error_handler(ex: ClientError):
    error, metadata = pluck(ex.response, 'Error', 'ResponseMetadata')
    status_code, error_code, message = (
        opt(metadata)['HTTPStatusCode'].value(),
        opt(error)['Code'].value(),
        opt(error)['Message'].value()
    )
    return ClientErrorResponse(status_code, error_code, message)
