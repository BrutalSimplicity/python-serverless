from typing import Any, Mapping, cast
from swawesomo.common.models import from_dict
from swacorp.ec.artifact_registry.api.deployment_plans.models import (
    AddArtifactToDeploymentPlanRequest,
    CreateOrUpdateDeploymentPlanRequest,
    DeleteArtifactForDeploymentPlanRequest,
    GetDeploymentPlanQueryRequest,
    GetDeploymentPlanRequest,
    TriggerDeploymentPlanRequest,
)
from swacorp.ec.artifact_registry.aws.models import (
    ApiGatewayEventModel,
    ApiGatewayResponseModel,
    HttpMethod,
)

BASE_ROUTE = "deployments/plans"


def route(resource: str):
    return "/".join([BASE_ROUTE, resource])


def get_deployment_plan(request: GetDeploymentPlanRequest):
    return ApiGatewayResponseModel(200, request)


def get_deployment_plans(request: GetDeploymentPlanQueryRequest):
    return ApiGatewayResponseModel(200, request)


def create_or_update_deployment_plan(request: CreateOrUpdateDeploymentPlanRequest):
    return ApiGatewayResponseModel(201, request)


def add_artifact_to_deployment_plan(request: AddArtifactToDeploymentPlanRequest):
    return ApiGatewayResponseModel(201, request)


def delete_artifact_from_deployment_plan(
    request: DeleteArtifactForDeploymentPlanRequest,
):
    return ApiGatewayResponseModel(204, request)


def trigger_deployment(request: TriggerDeploymentPlanRequest):
    return ApiGatewayResponseModel(201, request)


def handler(event: ApiGatewayEventModel):
    if event.match_route(HttpMethod.GET, route("{selector}")):
        return get_deployment_plan(
            from_dict(GetDeploymentPlanRequest, event.parameters)
        )

    if event.match_route(HttpMethod.GET, route("")):
        return get_deployment_plans(
            from_dict(GetDeploymentPlanQueryRequest, event.query_parameters)
        )
    if event.match_route(HttpMethod.POST, route("")):
        return create_or_update_deployment_plan(
            from_dict(
                CreateOrUpdateDeploymentPlanRequest, cast(Mapping[str, Any], event.body)
            )
        )
    if event.match_route(HttpMethod.POST, route("{selector}/artifact/{artifact_key}")):
        return add_artifact_to_deployment_plan(
            from_dict(AddArtifactToDeploymentPlanRequest, event.path_parameters)
        )
    if event.match_route(
        HttpMethod.DELETE,
        route("{selector}/artifact/{artifact_key}"),
    ):
        return delete_artifact_from_deployment_plan(
            from_dict(DeleteArtifactForDeploymentPlanRequest, event.path_parameters)
        )
    if event.match_route(HttpMethod.POST, route("_trigger")):
        return trigger_deployment(
            from_dict(TriggerDeploymentPlanRequest, cast(Mapping[str, Any], event.body))
        )
