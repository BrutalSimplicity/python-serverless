from boto3.dynamodb.conditions import ConditionBase
from dataclasses import dataclass
from typing import Optional


@dataclass
class DynamoDBQuery:
    key_condition: ConditionBase
    sort_condition: Optional[ConditionBase]


@dataclass
class DynamoDBEntity:
    PK: str
    SK: str
    GSI1PK: Optional[str]
    GSI1SK: Optional[str]
