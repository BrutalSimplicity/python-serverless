import unittest
from unittest.mock import MagicMock

from boto3.dynamodb.conditions import Key
from cloudtools.aws.dynamodb import DynamodbConnector
from cloudtools.aws.dynamodb import DynamodbCollection, PagingParameters

class DynamodTests(unittest.TestCase):

    def test_should_return_entities_within_limit(self):
        connector = DynamodbConnector(MagicMock(), 'test')
        connector.table.query.side_effect = [
            {'Items': [1, 2, 3, 4, 5], 'LastEvaluatedKey': 'key'}
        ]

        results = connector._make_query(Key('test').eq('value'), PagingParameters(5, False))
        actual = (results.items, results.last_evaluated_key)

        self.assertCountEqual(actual, ([1, 2, 3, 4, 5], 'key'))

    def test_should_return_all_entities(self):
        connector = DynamodbConnector(MagicMock(), 'test')
        connector.table.query.side_effect = [
            {'Items': [1, 2, 3, 4, 5], 'LastEvaluatedKey': 'key'},
            {'Items': [6, 7, 8, 9, 10], 'LastEvaluatedKey': None},
        ]

        results = connector._make_query(Key('test').eq('value'), PagingParameters(100, False))
        actual = (results.items, results.last_evaluated_key)

        self.assertCountEqual(actual, ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], None))

    def test_should_return_all_results_when_last_evaluated_key_is_none(self):
        connector = DynamodbConnector(MagicMock(), 'test')
        connector.table.query.side_effect = [
            {'Items': [1, 2, 3, 4, 5], 'LastEvaluatedKey': None},
        ]

        results = list(connector._make_query(Key('test').eq('value'), PagingParameters(100, False)))

        self.assertCountEqual(results, [1, 2, 3, 4, 5], results)

    def test_should_paginate_through_results_as_iterator(self):
        connector = DynamodbConnector(MagicMock(), 'test')
        connector.table.query.side_effect = [
            {'Items': [1, 2, 3, 4, 5], 'LastEvaluatedKey': 'key'},
            {'Items': [6, 7, 8, 9, 10], 'LastEvaluatedKey': None},
        ]

        paginator = connector._make_query(Key('test').eq('value'), PagingParameters(5, False))

        self.assertIsInstance(paginator, DynamodbCollection)
        self.assertEqual(paginator.items, [1, 2, 3, 4, 5])
        self.assertEqual(paginator.last_evaluated_key, 'key')

        results = list(paginator)

        self.assertCountEqual(results, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_should_paginate_through_results_as_iterator_for_limit_of_one(self):
        connector = DynamodbConnector(MagicMock(), 'test')
        connector.table.query.side_effect = [
            {'Items': [1], 'LastEvaluatedKey': 'key'},
            {'Items': [2], 'LastEvaluatedKey': 'key'},
            {'Items': [3], 'LastEvaluatedKey': 'key'},
            {'Items': [4], 'LastEvaluatedKey': 'key'},
            {'Items': [5], 'LastEvaluatedKey': 'key'},
            {'Items': [6], 'LastEvaluatedKey': None},
        ]

        paginator = connector._make_query(Key('test').eq('value'), PagingParameters(1, False))

        self.assertIsInstance(paginator, DynamodbCollection)
        self.assertEqual(paginator.items, [1])
        self.assertEqual(paginator.last_evaluated_key, 'key')

        results = list(paginator)

        self.assertCountEqual(results, [1, 2, 3, 4, 5, 6])
