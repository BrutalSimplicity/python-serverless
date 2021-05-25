import pytest
from swacorp.ec.artifact_registry.artifacts.connector import ArtifactEntityDocument
from swawesomo.aws.dynamodb.models import PagingParameters

from swacorp.ec.artifact_registry.aws.dynamodb.models import DynamoDBQuery


@pytest.fixture
def artifacts_query():
    paging = PagingParameters(10, False)
    return ArtifactEntityDocument.create_query(None, None, paging)


def test_artfiacts_query(artifacts_query: DynamoDBQuery):
    expression = artifacts_query.key_condition.get_expression()
    assert expression
    assert artifacts_query.index == None
    assert artifacts_query.paging
