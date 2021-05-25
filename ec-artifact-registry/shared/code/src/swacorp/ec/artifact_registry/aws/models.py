import enum
from base64 import b64decode
from dataclasses import dataclass, field
from typing import Any, List, Mapping, Optional, Tuple, Union, cast
from swawesomo.common.json import decoder, encoder
from swawesomo.common.optional import OptionalHandler as opt
from swawesomo.common.utils import convert_to_dict, walk_keys


class HttpMethod(str, enum.Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    ANY = "ANY"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


@dataclass
class ApiGatewayEventModel:
    request_id: str
    identity: str
    host: str
    resource: str
    path: str
    method: HttpMethod
    body: Optional[Union[bytes, str, Mapping[str, Any]]]
    headers: Mapping[str, Union[str, List[str]]]
    parameters: Mapping[str, Union[str, List[str]]]
    query_parameters: Mapping[str, Union[str, List[str]]]
    path_parameters: Mapping[str, str]
    stage: str
    stage_variables: Mapping[str, str]
    timestamp: int

    def match_route(
        self,
        method: HttpMethod,
        route: str,
        parameters: Optional[Mapping[str, Any]] = None,
    ):
        resource = self.resource.lstrip("/")
        route = route.lstrip("/")
        if self.method != method or resource != route:
            return False
        if parameters and not all(
            [key in self.parameters for key in parameters.keys()]
        ):
            return False
        return True

    @classmethod
    def create(cls, event: Mapping[str, Any]):
        optevent = opt(event)
        query_params = _get_query_params(optevent)
        path_params = _get_path_params(optevent)
        context = optevent["requestContext"]

        return ApiGatewayEventModel(
            resource=event["resource"],
            path=event["path"],
            method=event["httpMethod"],
            body=_get_body(optevent),
            headers=_get_headers(optevent),
            host=optevent["host"].value(),
            request_id=cast(str, context["requestId"].value()),
            identity=cast(str, context["identity"]["userArn"].value()),
            query_parameters=query_params,
            path_parameters=_get_path_params(optevent),
            parameters=cast(Any, _merge_params(query_params, path_params)),
            stage=cast(str, context["stage"].value()),
            stage_variables=cast(
                Mapping[str, str], optevent["stageVariables"].value({})
            ),
            timestamp=cast(int, context["timestamp"].value(0)),
        )


def _get_headers(event):
    headers = event["headers"].value({})
    multi = event["multiValueHeaders"].value({})
    for header in headers:
        if header in multi and len(multi[header]) > 1:
            headers[header] = multi[header]

    return headers


def _get_body(event):
    body = event["body"].value()
    if not body:
        return None

    if event["isBase64Encoded"]:
        body = b64decode(body).decode("utf8")

    is_json = isinstance(body, str) and body.startswith("{")
    if is_json:
        return cast(Mapping[str, Any], decoder(body))

    return cast(str, body)


def _get_query_params(event):
    params = event["queryStringParameters"].value({})
    multi = event["multiValueQueryStringParameters"].value({})
    for param in params:
        if param in multi and len(multi[param]) > 1:
            params[param] = multi[param]

    return params


def _get_path_params(event):
    return event["pathParameters"].value({})


def _merge_params(query, path):
    result = cast(dict, path).copy()
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


def convert_snakecase_to_camelcase(item: Tuple[str, Any]):
    key, value = item[0], item[1]

    key = key.strip("_")

    prev = key[0]
    result = prev
    for next in key[1:]:
        if prev == "_" and next != "_":
            result += next.upper()
        elif next != "_":
            result += next
        prev = next

    return result, value


@dataclass
class ApiGatewayResponseModel:
    statusCode: int
    body: Any
    headers: Mapping[str, Any] = field(
        default_factory=lambda: {"Content-Type": "application/json"}
    )
    isBase64Encoded: bool = field(default=False)

    def __post_init__(self):
        body_dict = convert_to_dict(self.body)
        body_dict = walk_keys(
            cast(Any, body_dict), lambda k, v: convert_snakecase_to_camelcase((k, v))
        )
        self.body = encoder(body_dict)


@dataclass
class S3EventModel:
    bucket: str
    owner: str
    bucket_arn: str
    key: str
    version: str
    etag: str

    @classmethod
    def create(cls, event):
        optevent = opt(event)
        return S3EventModel(
            bucket=optevent["s3"]["bucket"]["name"].value(),
            owner=optevent["s3"]["bucket"]["ownerIdentity"].value(),
            bucket_arn=optevent["s3"]["bucket"]["arn"].value(),
            key=optevent["s3"]["object"]["key"].value(),
            version=optevent["s3"]["object"]["versionId"].value(),
            etag=optevent["s3"]["object"]["eTag"].value(),
        )


@dataclass
class EventBridgeEventModel:
    pass


@dataclass
class StepFunctionEventModel:
    pass
