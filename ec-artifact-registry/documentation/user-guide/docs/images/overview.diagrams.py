from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway, Route53
from diagrams.aws.storage import SimpleStorageServiceS3

import os
from pathlib import Path

graph_attr = {
    "bgcolor": "transparent",
    "center": "true"
}


with Diagram(name="New Account Artifact Registry", show=False, outformat="png", graph_attr=graph_attr):

    with Cluster("DDE Account"):

        registry_route_53 = Route53("registry.ec.{env}.swacorp.com")

        with Cluster("Green Deployment", graph_attr={
            "bgcolor": "#A9F5BC"
        }):
            registry_api_gateway_green = APIGateway("Registry")

            registry_route_53 >> Edge(label="Active") >> registry_api_gateway_green

        with Cluster("Blue Deployment", graph_attr={
            "bgcolor": "#A9BCF5"
        }):
            registry_api_gateway_blue = APIGateway("Registry")

            registry_route_53 >> Edge(label="Inactive") >> registry_api_gateway_blue
