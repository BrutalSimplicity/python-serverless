from dataclasses import dataclass
import unittest
from unittest.mock import MagicMock
from cloudtools.common.lazy import Lazy

class LazyTests(unittest.TestCase):
    def test_should_lazily_resolve_function_call(self):
        def get_data():
            return 'lots of data'

        datafn = Lazy(lambda: get_data())

        self.assertIsInstance(datafn, Lazy)

        actual = datafn()

        self.assertEqual(get_data(), actual)

    def test_should_lazily_resolve_key_lookup(self):
        data = {
            'exists': True
        }

        lazy = Lazy(lambda: data)

        def get_value():
            return lazy['yettoexist']

        data['yettoexist'] = True

        self.assertTrue(get_value())

    def test_should_lazily_resolve_attribute_lookup(self):
        @dataclass
        class Record:
            data: str

        def get_expensive_object():
            return Record('test')

        obj = Lazy(lambda: get_expensive_object())

        self.assertEqual('test', obj.data)

    def test_should_only_resolve_value_once(self):
        magic = MagicMock()
        magic.return_value = True

        lazy = Lazy(lambda: magic())

        value = lazy()

        self.assertTrue(lazy())
        self.assertTrue(value)

        magic.assert_called_once()
