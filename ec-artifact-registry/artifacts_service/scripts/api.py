import pathfix  # noqa: F401
import json
import os
from pathlib import Path
from typing import Any, Dict, Mapping, Optional
from yaml import load
from yaml.loader import Loader

import click
import requests
import simplejson
from aws_requests_auth.aws_auth import AWSRequestsAuth
from swawesomo.common.utils import filter_empty_properties

DEPLOY_ENVIRONMENT = os.environ.get("DEPLOY_ENVIRONMENT", "dev").lower()
API_ENDPOINT = f"https://api.registry.ec.{DEPLOY_ENVIRONMENT}.aws.swacorp.com"
if DEPLOY_ENVIRONMENT.lower() not in ["dev", "qa", "prod"]:
    API_ENDPOINT = f"https://{DEPLOY_ENVIRONMENT}.api.registry.ec.dev.aws.swacorp.com"
REGION = (
    os.environ.get("AWS_REGION") or os.environ.get("DEFAULT_AWS_REGION") or "us-east-1"
)
SWA_CERT = (
    os.path.join(Path(__file__).parent, "swadevrootca1.pem")
    if DEPLOY_ENVIRONMENT not in ["qa", "prod"]
    else os.path.join(Path(__file__).parent, f"swa{DEPLOY_ENVIRONMENT}rootca1.pem")
)


def _make_api_call(
    invoke_url: str,
    http_method: str = "get",
    params: Optional[Mapping[str, str]] = None,
    headers: Mapping[str, str] = {},
    body: Mapping[str, Any] = None,
):
    print(invoke_url)
    host = invoke_url.replace("https://", "").split("/")[0]
    auth = AWSRequestsAuth(
        aws_access_key=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        aws_token=os.environ["AWS_SESSION_TOKEN"],
        aws_host=host,
        aws_region=REGION,
        aws_service="execute-api",
    )
    if http_method == "get":
        return requests.get(
            url=invoke_url, auth=auth, params=params, headers=headers, verify=SWA_CERT
        )
    if http_method == "post":
        return requests.post(
            url=invoke_url,
            auth=auth,
            params=params,
            headers=headers,
            data=body,
            verify=SWA_CERT,
        )


def collection_to_output(collection: Dict[str, Any]):
    if "items" in collection:
        collection["count"] = len(collection["items"])
        return collection
    return collection


def printjson(data):
    print(simplejson.dumps(data, indent="  "))


@click.group(
    help="""
Use to interact with the API

pipenv run python api.py events etag
"""
)
def cli():
    pass


@cli.command()
@click.argument("etag")
@click.option("-s", "--selectors", type=str)
@click.option("-n", "--limit", type=int, default=10, show_default=True)
@click.option("-o", "--ascending", type=bool, default=False, show_default=True)
@click.option("-k", "--lastkey", type=str)
def deployments(selector, limit, ascending, lastkey):
    route = "/registry/deployments"
    path = "/".join(filter(None, [API_ENDPOINT, route, selector]))
    params = filter_empty_properties(
        {
            "limit": limit,
            "ascending": "true" if ascending else None,
            "lastEvaluatedKey": lastkey,
        }
    )
    response = _make_api_call(path, params=params)
    printjson(collection_to_output(response.json()))


@cli.command()
@click.argument("selector")
@click.argument("artifact_file")
def update(selector, artifact_file):
    route = "/registry/deployment"
    path = "/".join([API_ENDPOINT, route, selector])
    if not os.path.exists(artifact_file):
        raise Exception(f"artifact_file does not exist: {artifact_file}")
    if not os.path.isfile(artifact_file):
        raise Exception(f"artifact_file is not a file: {artifact_file}")
    with open(artifact_file) as fd:
        if artifact_file.endswith("yml") or artifact_file.endswith("yaml"):
            data = load(fd, Loader)
        elif artifact_file.endswith("json"):
            data = json.loads(fd.read())
        else:
            raise Exception("artifact_file must be json or yaml")

    response = _make_api_call(path, "post", body={})
    printjson(response.json())


@cli.command()
@click.argument("s3_url")
def get_presigned_url(s3_url):
    route = "/registry/artifacts"
    path = "/".join([API_ENDPOINT, route, "presigned_url"])
    params = {"s3_url": s3_url}
    response = _make_api_call(path, params=params)
    printjson(response.json())


if __name__ == "__main__":
    cli()
