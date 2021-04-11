from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
    cast,
    overload,
)

from boto3.dynamodb.conditions import ConditionBase
from botocore.exceptions import ClientError

from cloudtools.common.optional import OptionalHandler as opt

from .models import (
    DynamodbPaginator,
    DynamodbResource,
    PagingParameters,
    ScanPagingParameters,
)

T = TypeVar("T")


class MissingKeysError(Exception):
    pass


class DynamodbConnector:
    def __init__(self, dynamodb: DynamodbResource, table_name: str):
        self.dynamodb = dynamodb
        self.table = self.dynamodb.Table(table_name)

    def _put_item(
        self,
        item: Mapping[str, Any],
        condition_expressions: Optional[Sequence[ConditionBase]] = None,
    ):

        if condition_expressions:
            for condition in condition_expressions:
                try:
                    self.table.put_item(Item=item, ConditionExpression=condition)
                except ClientError as err:
                    if (
                        err.response["Error"]["Code"]
                        == "ConditionalCheckFailedException"
                    ):
                        continue
                    raise err
        else:
            self.table.put_item(Item=item)

    @overload
    def _make_query(
        self,
        key_condition: ConditionBase,
        paging: PagingParameters,
        filter_condition: Optional[ConditionBase] = None,
        index: str = None,
    ) -> DynamodbPaginator[Dict[str, Any]]:
        ...

    @overload
    def _make_query(
        self,
        key_condition: ConditionBase,
        paging: PagingParameters,
        mapper: Callable[[Any], T],
        filter_condition: Optional[ConditionBase] = None,
        index: str = None,
    ) -> DynamodbPaginator[T]:
        ...

    def _make_query(
        self,
        key_condition: ConditionBase,
        paging: PagingParameters,
        filter_condition: Optional[ConditionBase] = None,
        index: str = None,
        mapper=None,
    ):
        def internal_make_query(key_condition, paging, filter_condition, index):
            limit = min(paging.limit, 100)
            entities = []
            should_continue = True
            last_key_evaluated = paging.last_evaluated_key

            while should_continue:
                kwargs = {
                    "IndexName": index,
                    "KeyConditionExpression": key_condition,
                    "ScanIndexForward": paging.ascending,
                    "ExclusiveStartKey": last_key_evaluated,
                    "Limit": limit,
                    "FilterExpression": filter_condition,
                }
                kwargs = {k: v for k, v in kwargs.items() if v is not None}

                response = self.table.query(**kwargs)
                items, last_key_evaluated = (
                    response["Items"],
                    opt(response)["LastEvaluatedKey"].value(),
                )
                entities.extend(items)
                should_continue = (
                    True if last_key_evaluated and len(entities) < limit else False
                )

            return cast(List[Dict[str, Any]], entities), cast(
                Dict[str, Any], last_key_evaluated
            )

        def next(key):
            results, last_key = internal_make_query(
                key_condition,
                PagingParameters(paging.limit, paging.ascending, key),
                filter_condition,
                index,
            )
            if mapper:
                return [mapper(item) for item in results], last_key
            return results, last_key

        results, last_key = next(paging.last_evaluated_key)

        return DynamodbPaginator(items=results, last_evaluated_key=last_key, next=next)

    @overload
    def _make_scan(
        self, filter_condition: ConditionBase, paging: ScanPagingParameters
    ) -> DynamodbPaginator[Dict[str, Any]]:
        ...

    @overload
    def _make_scan(
        self,
        filter_condition: ConditionBase,
        paging: ScanPagingParameters,
        mapper: Callable[[Any], T],
    ) -> DynamodbPaginator[T]:
        ...

    def _make_scan(
        self, filter_condition: ConditionBase, paging: ScanPagingParameters, mapper=None
    ):
        def internal_make_scan(filter_condition, paging):
            limit = min(paging.limit, 100)
            entities = []
            should_continue = True
            last_key_evaluated = paging.last_evaluated_key

            while should_continue:
                kwargs = {
                    "ExclusiveStartKey": last_key_evaluated,
                    "Limit": limit,
                    "FilterExpression": filter_condition,
                }
                kwargs = {k: v for k, v in kwargs.items() if v is not None}

                response = self.table.scan(**kwargs)
                items, last_key_evaluated = (
                    response["Items"],
                    opt(response)["LastEvaluatedKey"].value(),
                )
                entities.extend(items)
                should_continue = (
                    True if last_key_evaluated and len(entities) < limit else False
                )

            return cast(List[Dict[str, Any]], entities), cast(
                Dict[str, Any], last_key_evaluated
            )

        def next(key):
            results, last_key = internal_make_scan(
                filter_condition, ScanPagingParameters(paging.limit, key)
            )
            if mapper:
                return [mapper(item) for item in results], last_key
            return results, last_key

        results, last_key = next(paging.last_evaluated_key)

        return DynamodbPaginator(items=results, last_evaluated_key=last_key, next=next)

    def _make_key(self, *args: Optional[str], ignore_missing_keys=False) -> str:
        if ignore_missing_keys or all(args):
            keys = [k for k in args if k]
            return "#".join(cast(str, keys))

        raise MissingKeysError(f"One of the keys is missing data: [{args}]")
