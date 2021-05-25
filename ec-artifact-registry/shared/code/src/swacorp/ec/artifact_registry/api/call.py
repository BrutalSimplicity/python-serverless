from swawesomo.common.logging import log_it
import requests
from typing import Optional, Mapping
from aws_requests_auth.aws_auth import AWSRequestsAuth
from swacorp.ec.artifact_registry.api.session import SessionParams


@log_it
def make_api_call(
    sesh: SessionParams,
    resource: str,
    params: Optional[Mapping[str, str]] = None,
    headers: Mapping[str, str] = {},
    method: str = "GET",
):
    invoke_url = "/".join([sesh._endpoint, resource])
    host = invoke_url.replace("https://", "").split("/")[0]
    credentials = sesh._session.get_credentials()
    auth = AWSRequestsAuth(
        aws_access_key=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_token=credentials.token,
        aws_host=host,
        aws_region=sesh._session.region_name,
        aws_service="execute-api",
    )
    response = requests.request(
        method=method,
        url=invoke_url,
        auth=auth,
        params=params,
        headers=headers,
        verify=sesh._swacert,
    )

    return response.json()
