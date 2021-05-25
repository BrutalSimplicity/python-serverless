from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import Route53
from diagrams.aws.storage import SimpleStorageServiceS3
from diagrams.aws.database import Dynamodb
from diagrams.onprem.client import User

graph_attr = {
    "bgcolor": "transparent",
    "center": True
    }

with Diagram(name="Create Update Registry Artifact", show=False, outformat="png", graph_attr=graph_attr):

    client = User()

    with Cluster("DDE Account"):

        registry_route_53 = Route53("registry.ec.{env}.swacorp.com")

        with Cluster("Artifact Registry"):

            api_lambda = Lambda("API")
            artifact_updater_lambda = Lambda("Artifact Updater")
            artifact_registry_s3 = SimpleStorageServiceS3("Artifact Registry")
            artifact_registry_ddb = Dynamodb("Artifact Registry")

            client >> Edge(label="3 POST") >> artifact_registry_s3 >> Edge(label="4 S3 Event", style="dashed") >> artifact_updater_lambda >> artifact_registry_ddb  # noqa E501
            client << registry_route_53 << Edge(label="2 Presigned URL") << api_lambda
            client >> Edge(label="1 GeneratePresignedURL") >> registry_route_53 >> api_lambda

    client >> registry_route_53 >> api_lambda
