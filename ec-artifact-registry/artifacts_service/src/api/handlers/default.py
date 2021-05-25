from swacorp.ec.artifact_registry.aws.models import (
    ApiGatewayEventModel,
    ApiGatewayResponseModel,
)


def handler(event: ApiGatewayEventModel):
    return ApiGatewayResponseModel(
        404, {"message": "No handler found matching the request"}
    )
