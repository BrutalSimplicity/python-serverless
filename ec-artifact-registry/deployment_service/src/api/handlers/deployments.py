from typing import Any, Mapping, cast
from swawesomo.common.models import from_dict
from swacorp.ec.artifact_registry.api.deployments.models import (
    GetDeploymentStatusQueryRequest,
    GetDeploymentStatusRequest,
)
from swacorp.ec.artifact_registry.aws.models import (
    ApiGatewayEventModel,
    ApiGatewayResponseModel,
    HttpMethod,
)

BASE_ROUTE = "deployments"


def _route(resource: str):
    return "/".join([BASE_ROUTE, resource])


def get_deployment_status(request: GetDeploymentStatusRequest):
    return ApiGatewayResponseModel(200, request)


def get_deployments(request: GetDeploymentStatusQueryRequest):
    return ApiGatewayResponseModel(200, request)


def handler(event: ApiGatewayEventModel):
    if event.match_route(HttpMethod.GET, _route("{id}")):
        return get_deployment_status(
            from_dict(GetDeploymentStatusRequest, event.parameters)
        )

    if event.match_route(HttpMethod.GET, _route("")):
        return get_deployments(
            from_dict(GetDeploymentStatusQueryRequest, event.parameters)
        )
