from base64 import b64decode
from dataclasses import dataclass
from typing import Any, List, Mapping, Optional, Union, cast
from cloudtools.common.json import decoder

@dataclass
class ApiGatewayEventModel:
    request_id: str
    host: str
    path: str
    method: str
    body: Optional[Union[bytes, str, Mapping[str, Any]]]
    headers: Mapping[str, Union[str, List[str]]]
    parameters: Mapping[str, Union[str, List[str]]]
    query_parameters: Mapping[str, Union[str, List[str]]]
    path_parameters: Mapping[str, str]
    stage: str
    stage_variables: Mapping[str, str]
    timestamp: int

    @classmethod
    def create(cls, event: Mapping[str, Any]):
        query_params = _get_query_params(event)
        path_params = _get_path_params(event)
        context = event.get('requestContext', {})

        return ApiGatewayEventModel(
            path=event['path'],
            method=event['httpMethod'],
            body=_get_body(event),
            headers=_get_headers(event),
            host=event['host'],
            request_id=cast(str, context.get('requestId')),
            query_parameters=query_params,
            path_parameters=_get_path_params(event),
            parameters=cast(Any, _merge_params(query_params, path_params)),
            stage=cast(str, context.get('stage')),
            stage_variables=cast(Mapping[str, str], event.get('stageVariables')),
            timestamp=cast(int, context.get('timestamp'))
        )

def _get_headers(event):
    headers = event.get('headers', {})
    multi = event.get('multiValueHeaders', {})
    for header in headers:
        if header in multi and len(multi[header]) > 1:
            headers[header] = multi[header]

    return headers


def _get_body(event):
    body = event.get('body')
    if not body:
        return None

    if event['isBase64Encoded']:
        body = b64decode(body).decode('utf8')

    is_json = isinstance(body, str) and body.startswith('{')
    if is_json:
        return cast(Mapping[str, Any], decoder(body))

    return cast(str, body)

def _get_query_params(event):
    params = event.get('queryStringParameters', {})
    multi = event.get('multiValueQueryStringParameters', {})
    for param in params:
        if param in multi and len(multi[param]) > 1:
            params[param] = multi[param]

    return params

def _get_path_params(event):
    return event.get('pathParameters', {})

def _merge_params(query, path):
    result = path
    for key, value in query.items():
        if key in result:
            if isinstance(result[key], list):
                if isinstance(value, list):
                    result[key].extend(value)
                else:
                    result[key] = [*result[key], value]
            else:
                if isinstance(value, list):
                    result[key] = [result[key], *value]
                else:
                    result[key] = [result[key], value]
        else:
            result[key] = value
    return result
