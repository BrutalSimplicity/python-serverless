import unittest
import itertools

from cloudtools.common.utils import pluck, retry, walk_keys

class UtilsTests(unittest.TestCase):

    def test_pluck_should_grab_values_for_keys(self):
        input = {
            'a': 1,
            'b': 2,
            'c': 3
        }

        a, b, c, d = pluck(input, 'a', 'b', 'c', 'd')

        self.assertEqual(a, 1)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertIsNone(d)

    def test_should_retry_fn_max_times(self):
        class MaxRetriesException(Exception):
            pass

        tries = 0
        @retry(max_retries=5, delay_seconds=0)
        def action():
            nonlocal tries
            tries += 1
            raise MaxRetriesException()

        with self.assertRaises(MaxRetriesException):
            action()

    def test_should_not_retry_excluded_exceptions(self):
        class ActualException(Exception):
            pass

        class ExpectedExceptin(Exception):
            pass

        tries = 0
        @retry(max_retries=5, delay_seconds=0, allowable_exceptions=[ExpectedExceptin])
        def action():
            nonlocal tries
            tries += 1
            raise ActualException()

        with self.assertRaises(ActualException):
            action()

    def test_should_walk_keys_for_mapping(self):
        data = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': {
                'e': 4,
                'f': 5,
                'g': [
                    {
                        'h': 6,
                        'i': 7
                    }
                ]
            }
        }

        expected = {
            '_a_': 1,
            '_b_': 2,
            '_c_': 3,
            '_d_': {
                '_e_': 4,
                '_f_': 5,
                '_g_': [
                    {
                        '_h_': 6,
                        '_i_': 7
                    }
                ]
            }
        }

        actual = walk_keys(data, lambda key, _: (f'_{key}_', None))

        self.assertCountEqual(expected, actual)

    def test_should_walk_keys_for_sequence(self):
        data = [
            {
                'a': 1,
                'b': 2,
                'c': 3,
            },
            {
                'd': 4,
                'e': 5,
                'f': 6
            },
            {
                'g': (1, 2, 3, 4),
                'h': {
                    'i': list(itertools.repeat({'j': 1}, 10))
                }
            }
        ]

        expected = [
            {
                '_a_': 1,
                '_b_': 2,
                '_c_': 3,
            },
            {
                '_d_': 4,
                '_e_': 5,
                '_f_': 6
            },
            {
                '_g_': (1, 2, 3, 4),
                '_h_': {
                    '_i_': list(itertools.repeat({'_j_': 1}, 10))
                }
            }
        ]

        actual = walk_keys(data, lambda key, _: (f'_{key}_', None))

        self.assertCountEqual(expected, actual)
