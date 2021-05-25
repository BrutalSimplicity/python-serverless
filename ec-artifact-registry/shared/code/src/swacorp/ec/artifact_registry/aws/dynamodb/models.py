import logging
from swawesomo.common.utils import filter_empty_properties
from swawesomo.aws.dynamodb.models import PagingParameters
from dataclasses import dataclass, asdict
from typing import Optional
from swacorp.ec.artifact_registry.logging import log_it

from boto3.dynamodb.conditions import ConditionBase
from boto3.dynamodb.conditions import Key


@dataclass
class DynamoDBQuery:
    key_condition: ConditionBase
    paging: PagingParameters
    index: Optional[str] = None

    def to_query(self):
        return {
            "key_condition": self.key_condition,
            "index": self.index,
            "paging": self.paging,
        }


@dataclass
class DynamoDBEntity:
    PK: str
    SK: str
    GSI1PK: Optional[str]
    GSI1SK: Optional[str]

    def to_key(self):
        result = asdict(self)
        return filter_empty_properties(result)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def PartitionKey(cls):
        return Key("PK")

    @classmethod
    def SortKey(cls):
        return Key("SK")

    @classmethod
    def GlobalSecondaryIndexOne(cls):
        return "GSI1"

    @classmethod
    def GlobalSecondaryIndexOnePartitionKey(cls):
        return Key("GSI1PK")

    @classmethod
    def GlobalSecondaryIndexOneSortKey(cls):
        return Key("GSI1SK")


class TooManyArgumentsError(Exception):
    pass


class FailOnConsecutiveMissingKeysError(Exception):
    pass


class KeyGenerator:
    def __init__(self, *prefixes: str):
        self._prefixes = prefixes

    @log_it(level=logging.DEBUG)
    def generate(
        self, *args: Optional[str], fail_on_consecutive_missing_keys: bool = True
    ) -> str:
        def has_consecutive_keys(keys):
            return all(
                [
                    any((keys[i], keys[i + 1] if i + 1 < len(keys) else True))
                    for i in range(len(keys))
                ]
            )

        if args and len(args) > len(self._prefixes):
            raise TooManyArgumentsError(
                f"Too many args for the number of prefixes (prefixes: {self._prefixes}, args: {args}"
            )

        if args and any([k for k in args if k]):
            if fail_on_consecutive_missing_keys and not has_consecutive_keys(args):
                raise FailOnConsecutiveMissingKeysError(
                    "There are consecutive missing keys. Set `fail_on_consecutive_missing_keys` to false to ignore this error."
                )
            return "#".join(
                [item for pair in zip(self._prefixes, args) for item in pair if item]
            )

        return self._prefixes[0]
